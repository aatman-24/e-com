// ---------- helpers ----------
function wait(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function realClick(el) {
  ["pointerdown", "mousedown", "mouseup", "click"].forEach((type) => {
    el.dispatchEvent(
      new MouseEvent(type, { bubbles: true, cancelable: true, view: window })
    );
  });
}

function normalizeText(s) {
  return (s || "").replace(/\s+/g, " ").trim().toLowerCase();
}

// React-safe setter (works for controlled MUI inputs)
function setReactInputValue(input, value) {
  if (!input) return;
  const nativeSetter = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype,
    "value"
  ).set;
  const lastValue = input.value;
  nativeSetter.call(input, value);
  // fix React tracker if present (some React versions)
  const tracker = input._valueTracker;
  if (tracker && typeof tracker.setValue === "function")
    tracker.setValue(lastValue);
  input.dispatchEvent(new Event("input", { bubbles: true }));
  input.dispatchEvent(new Event("change", { bubbles: true }));
}


// ---------- robust searchable MUI dropdown selector ----------
/*
  inputElementOrId: either the <input readonly> element or its id (string)
  value: exact text to select (case-insensitive, trimmed)
*/
async function selectDropdownValueUniversal(
  inputElementOrId,
  value,
  opts = {}
) {
  const timeout = opts.timeout || 5000;
  const charDelay = opts.charDelay || 40; // typing speed
  const initialOpenDelay = opts.openDelay || 250;
  const postTypeDelay = opts.postTypeDelay || 450; // wait for filtering

  // resolve input element
  let input =
    typeof inputElementOrId === "string"
      ? document.getElementById(inputElementOrId)
      : inputElementOrId;

  if (!input) {
    console.warn(
      `⚠️ selectDropdownValueUniversal: input not found for "${inputElementOrId}"`
    );
    return false;
  }

  // blur anywhere to avoid aria-hidden/focus trap warnings
  if (document.activeElement) document.activeElement.blur();

  // 1) open the dropdown (simulate human)
  realClick(input);
  await wait(initialOpenDelay);


  // 2) find the menu container (prefer the Paper containing the search input or options)
  function findOpenMenu() {
    // common MUI menu containers (paper/popover/ul)
    const papers = Array.from(
      document.querySelectorAll(
        '.MuiPaper-root, .MuiPopover-root, ul.MuiMenu-list, div[role="menu"], div[role="presentation"]'
      )
    );
    // prefer one that contains a search input
    for (const p of papers) {
      if (
        p.querySelector('input[placeholder="Search"], input.MuiInputBase-input')
      )
        return p;
      if (p.querySelector("li.MuiMenuItem-root")) return p;
    }
    // fallback: any ul with role menu
    const u = document.querySelector('ul[role="menu"], ul.MuiMenu-list');
    if (u) return u;
    return null;
  }

  let menu = findOpenMenu();
  const start = Date.now();
  while (!menu && Date.now() - start < timeout) {
    await wait(120);
    menu = findOpenMenu();
  }
  if (!menu) {
    console.warn(
      `⚠️ Menu/portal not detected after opening dropdown for "${inputElementOrId}"`
    );
    return false;
  }

  // focus the menu if possible (reduce aria-hidden warnings)
  try {
    if (typeof menu.focus === "function") menu.focus();
  } catch (e) {}


  // 3) find search input inside that menu (if present) and type value char-by-char
  const searchSelectorCandidates = [
    'input[placeholder="Search"]',
    "input.MuiInputBase-input",
    'input[type="text"]',
  ];
  let searchBox = null;
  for (const sel of searchSelectorCandidates) {
    const found = menu.querySelector(sel);
    if (found) {
      searchBox = found;
      break;
    }
  }

  if (searchBox) {
    // clear then type the value slowly (helps React filtering)
    setReactInputValue(searchBox, "");
    searchBox.focus();
    await wait(80);
    // type char-by-char
    for (let i = 0; i < value.length; i++) {
      const prefix = value.slice(0, i + 1);
      setReactInputValue(searchBox, prefix);
      // also dispatch KeyboardEvents to better mimic user input (some libs listen)
      searchBox.dispatchEvent(new KeyboardEvent("keydown", { bubbles: true }));
      searchBox.dispatchEvent(new KeyboardEvent("keyup", { bubbles: true }));
      await wait(charDelay);
    }
    // final input event & small wait for filtering to apply
    searchBox.dispatchEvent(new Event("input", { bubbles: true }));
    await wait(postTypeDelay);
  } else {
    // if no search box, we rely on global options already present
    await wait(200);
  }

  // 4) Wait for the matching option to appear (retry loop)
  const valueNorm = normalizeText(value);
  let matchedEl = null;
  const maxTries = Math.ceil(timeout / 200);
  let tries = 0;
  while (!matchedEl && tries < maxTries) {
    // prefer options inside the menu if possible
    const optionNodes = menu
      ? Array.from(
          menu.querySelectorAll(
            'li[role="menuitem"], li.MuiMenuItem-root, [role="option"], [role="menuitem"]'
          )
        )
      : Array.from(
          document.querySelectorAll(
            'li[role="menuitem"], li.MuiMenuItem-root, [role="option"], [role="menuitem"]'
          )
        );

    // extract visible text from <p> or element textContent
    for (const opt of optionNodes) {
      const p = opt.querySelector("p");
      const text = p ? p.textContent : opt.textContent;
      if (!text) continue;
      if (normalizeText(text) === valueNorm) {
        matchedEl = opt;
        break;
      }
    }

    if (!matchedEl) {
      // try partial contains match (useful if option contains extra metadata)
      for (const opt of optionNodes) {
        const p = opt.querySelector("p");
        const text = p ? p.textContent : opt.textContent;
        if (!text) continue;
        if (normalizeText(text).includes(valueNorm)) {
          matchedEl = opt;
          break;
        }
      }
    }

    if (!matchedEl) {
      await wait(200);
      tries++;
    }
  }

  if (!matchedEl) {
    // final diagnostic: list first 10 option texts
    const allOptions = Array.from(
      document.querySelectorAll(
        'li[role="menuitem"] p, li.MuiMenuItem-root p, li[role="menuitem"], li.MuiMenuItem-root'
      )
    )
      .slice(0, 30)
      .map((e) => (e.textContent || e.innerText || "").trim());
    console.warn(
      `⚠️ Option "${value}" not found (searched ${tries} times). Nearby options:`,
      allOptions
    );
    return false;
  }

  // 5) click the match (use realClick)
  realClick(matchedEl);
  // wait until menu disappears (or short wait)
  const closeStart = Date.now();
  while (document.body.contains(matchedEl) && Date.now() - closeStart < 1500) {
    await wait(80);
  }
  await wait(140);
  return true;
}

// ---------- Row-by-row filler (uses the universal dropdown) ----------
async function fillFieldsByRow(fieldData) {
  const variations = document.querySelectorAll(".css-1hw3sau");
  const rows = variations.length
    ? Array.from(variations)
    : Array.from(document.querySelectorAll("div")).filter((d) =>
        d.querySelector("#meesho_price")
      );

  console.log(`Found ${rows.length} rows. Starting fill...`);
  const keys = Object.keys(fieldData);

  for (let r = 0; r < rows.length; r++) {
    const row = rows[r];
    console.log(`Filling row ${r + 1}/${rows.length}`);
    for (const key of keys) {
      const values = fieldData[key] || [];
      const value =
        values.length > 0
          ? values[r] !== undefined
            ? values[r]
            : values[values.length - 1]
          : undefined;
      if (value === undefined) continue;

      const input = row.querySelector(`#${key}`);
      if (!input) {
        console.warn(`Row ${r + 1}: no #${key} found; skipping`);
        continue;
      }

      console.log(`  - ${key} => "${value}"`);

      try {
        if (input.hasAttribute("readonly")) {
          // searchable dropdown flow
          const ok = await selectDropdownValueUniversal(input, String(value), {
            timeout: 6000,
          });
          if (!ok) console.warn(`Failed to set dropdown ${key} => ${value}`);
        } else {
          // text/number
          setReactInputValue(input, String(value));
        }
      } catch (err) {
        console.error(`Error setting ${key} in row ${r + 1}:`, err);
      }

      await wait(120);
    }
    await wait(180);
  }
  console.log("fillFieldsByRow completed ✅");
}

// ---------- USAGE ----------
// Example: provide the same `fieldData` object you used earlier (ids => arrays of 16 values)
// fillFieldsByRow();
// fillFieldsByRow({
//   meesho_price: [...],
//   weight: Array(16).fill("12-14"),
//   top_fabric: Array(16).fill("Cotton Blend"),
//   ...
// });