// ✅ Dropdown selector (handles <li><div><p> structure)
async function selectDropdownValue(inputId, value) {
  const input = document.getElementById(inputId);
  if (!input) {
    console.error(`❌ Input with id "${inputId}" not found`);
    return;
  }

  // Open dropdown
  input.click();
  await new Promise(r => setTimeout(r, 500));

  // Get all <li> options
  const options = Array.from(document.querySelectorAll('li.MuiMenuItem-root'));

  let matched = false;
  for (const option of options) {
    const textElement = option.querySelector('p'); // inside <p>
    if (textElement && textElement.textContent.trim() === value) {
      option.click();
      matched = true;
      break;
    }
  }

  if (!matched) {
    console.error(`❌ Option "${value}" not found for "${inputId}"`);
  }

  await new Promise(r => setTimeout(r, 300));
}

function setInputValue(id, value) {
  const input = document.getElementById(id);
  if (!input) {
    console.error(`❌ Input with id "${id}" not found`);
    return;
  }

  // Set value properly (works for React-controlled components)
  const lastValue = input.value;
  input.value = value;

  const event = new Event("input", { bubbles: true });
  // Hack for React 17+/18 synthetic event system
  const tracker = input._valueTracker;
  if (tracker) {
    tracker.setValue(lastValue);
  }
  input.dispatchEvent(event);

  console.log(`✅ Set "${id}" to "${value}"`);
}


// ✅ All field values go here
const fieldValues = {
  // Dropdowns
  top_color: "Blue",
  top_fabric: "Cotton Blend",
  bottom_color: "Red",
  bottom_fabric: "Cotton Blend",
  country_of_origin: "India",

  // Text inputs
  manufacturer_name: "Shop Sanskriti",
  manufacturer_address: "Surat",
  manufacturer_pincode: "395006",

  packer_name: "Shop Sanskriti",
  packer_address: "Surat",
  packer_pincode: "395006",

  multipack: "Single",  // Net quantity
  generic_name: "Kid's Clothing Set",
  set_type: "Top & Bottom Set"
};

// ✅ Auto-fill form function
async function autoFillForm(values) {
  // ---- Dropdowns ----
  await selectDropdownValue("top_color", values.top_color);
  await selectDropdownValue("top_fabric", values.top_fabric);
  await selectDropdownValue("bottom_color", values.bottom_color);
  await selectDropdownValue("bottom_fabric", values.bottom_fabric);
  await selectDropdownValue("country_of_origin", values.country_of_origin);
  await selectDropdownValue("generic_name", values.generic_name);
  await selectDropdownValue("multipack", values.multipack);
  await selectDropdownValue("set_type", values.set_type);

  // ---- Text inputs ----
  setInputValue("manufacturer_name", values.manufacturer_name);
  setInputValue("manufacturer_address", values.manufacturer_address);
  setInputValue("manufacturer_pincode", values.manufacturer_pincode);

  setInputValue("packer_name", values.packer_name);
  setInputValue("packer_address", values.packer_address);
  setInputValue("packer_pincode", values.packer_pincode);


  console.log("✅ Form auto-filled successfully!");
}

// 🚀 Run script
autoFillForm(fieldValues);
