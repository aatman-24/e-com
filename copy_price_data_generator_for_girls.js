import clipboard from 'clipboardy';

// ---------- Data generator ----------
function generateData(inputConfig) {
  const {
    count,
    meesho_price_start,
    product_mrp_global,
    inventory_global,
    product_id,
    top_chest_size_start,
    top_length_size_start,
    bottom_waist_size_start,
    bottom_length_size_start,
    weight
  } = inputConfig;

  let data = {
    meesho_price: [],
    only_wrong_return_price: [],
    product_mrp: [],
    inventory: [],
    supplier_sku_id: [],
    weight: weight,
    top_chest_size: [],
    top_length_size: [],
    bottom_waist_size: [],
    bottom_length_size: []
  };

  for (let i = 0; i < count; i++) {
    let price = meesho_price_start + (i * 10);
    data.meesho_price.push(price);
    data.only_wrong_return_price.push(price - 1);
    data.product_mrp.push(product_mrp_global);
    data.inventory.push(inventory_global);
    data.supplier_sku_id.push(`${product_id}_${i + 1}`);
    data.top_chest_size.push(top_chest_size_start + (i * 1));
    data.top_length_size.push(top_length_size_start + (i * 1));
    data.bottom_waist_size.push(bottom_waist_size_start + (i * 1));
    data.bottom_length_size.push(bottom_length_size_start + (i * 2));
  }

  return data;
}

// ---------- INPUT JSON (only edit this block) ----------
const inputConfig = {
  count: 16,
  meesho_price_start: 225,
  product_mrp_global: 999,
  inventory_global: 100,
  product_id: "girl_blank_pinch_cycle",
  top_chest_size_start: 19,
  top_length_size_start: 12,
  bottom_waist_size_start: 16,
  bottom_length_size_start: 18,
  weight: ["8-10","10-12","12-14","12-14","14-15","15-16","16-17","17-19","19-21","21-23","23-25","25-26","26-28","28-32","32-35","35-40"]
};

// ---------- Run ----------
const jsonData =  generateData(inputConfig);
clipboard.writeSync(JSON.stringify(jsonData, null, 2));