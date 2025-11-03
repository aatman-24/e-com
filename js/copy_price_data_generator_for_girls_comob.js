import clipboard from 'clipboardy';

// ---------- Data generator ----------
function generateData(inputConfig) {
  const {
    count,
    meesho_price,
    product_mrp_global,
    inventory_global,
    product_id,
    bust_size,
    waist_size,
    length_size,
    hip_size,
    weight
  } = inputConfig;

  let data = {
    meesho_price: meesho_price,
    only_wrong_return_price: [],
    product_mrp: [],
    inventory: [],
    supplier_sku_id: [],
    weight: weight,
    bust_size: bust_size,
    waist_size: waist_size,
    length_size: length_size,
    hip_size: hip_size
  };

  for (let i = 0; i < count; i++) {
    data.only_wrong_return_price.push(meesho_price[i] - 1);
    data.product_mrp.push(product_mrp_global);
    data.inventory.push(inventory_global);
    data.supplier_sku_id.push(`${product_id}_${i + 1}`);
    // bust_size, waist_size, length_size, hip_size are now taken directly from inputConfig arrays
  }

  return data;
}

// ---------- INPUT JSON (only edit this block) ----------
const inputConfig = {
  count: 16,
  meesho_price: [200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 320, 330, 340, 350, 360],
  product_mrp_global: 899,
  inventory_global: 100,
  product_id: "girl_black_white_combo",
  bust_size: [14, 14, 14, 14, 14, 14, 14, 14, 14, 15, 15, 16, 16, 17, 17, 18],
  waist_size: [13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 27, 28, 29, 30, 31],
  length_size: [19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 20, 21, 21, 22, 23, 24],
  hip_size: [15, 15, 15, 15, 15, 15, 15, 15, 15, 16, 16, 17, 17, 18, 19, 19],
  weight: ["8-10","10-12","12-14","12-14","14-15","15-16","16-17","17-19","19-21","21-23","23-25","25-26","26-28","28-32","32-35","35-40"]
};

// ---------- Run ----------
const jsonData =  generateData(inputConfig);
clipboard.writeSync(JSON.stringify(jsonData, null, 2));


