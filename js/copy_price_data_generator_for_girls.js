import clipboard from 'clipboardy';

// ---------- Data generator ----------
function generateData(inputConfig) {
  const {
    count,
    meesho_price,
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
    meesho_price: meesho_price,
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
    data.only_wrong_return_price.push(meesho_price[i] - 1);
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
  meesho_price: [200, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 325, 330, 335, 340],
  product_mrp_global: 899,
  inventory_global: 100,
  product_id: "girl_space_time_c4",
  top_chest_size_start: 19,
  top_length_size_start: 12,
  bottom_waist_size_start: 16,
  bottom_length_size_start: 18,
  weight: ["8-10","10-12","12-14","12-14","14-15","15-16","16-17","17-19","19-21","21-23","23-25","25-26","26-28","28-32","32-35","35-40"]
};

// ---------- Run ----------
const jsonData =  generateData(inputConfig);
clipboard.writeSync(JSON.stringify(jsonData, null, 2));