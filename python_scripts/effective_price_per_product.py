def calculate_effective_cost(product_cost, rto_rate, rto_loss_rate, 
                             customer_return_rate, customer_return_loss, gst, ads):
    """
    Calculate effective cost and break-even price (without shipping fee).

    product_cost: Cost of product for you
    rto_rate: % chance of RTO returns (0.10 = 10%)
    rto_loss_rate: % of RTO returns that actually cause product loss (0.02 = 2%)
    customer_return_rate: % chance of customer returns (0.10 = 10%)
    customer_return_loss: Loss per product when customer returns
    gst: GST per product
    ads: Ad cost per product
    """

    # Base cost (without shipping)
    base_cost = product_cost + gst + ads

    # Expected loss from RTO returns
    expected_rto_loss = product_cost * rto_rate * rto_loss_rate

    # Expected loss from customer returns
    expected_customer_loss = customer_return_rate * customer_return_loss

    # Effective cost
    effective_cost = base_cost + expected_rto_loss + expected_customer_loss

    return {
        "Base Cost (No Shipping)": round(base_cost, 2),
        "Expected RTO Loss": round(expected_rto_loss, 2),
        "Expected Customer Return Loss": round(expected_customer_loss, 2),
        "Effective Cost per Order (No Shipping)": round(effective_cost, 2),
        "Break Even Price (No Shipping)": round(effective_cost, 2)
    }

# Example usage with your data:
result = calculate_effective_cost(
    product_cost=170,
    rto_rate=0.10,
    rto_loss_rate=0.02,
    customer_return_rate=0.12,
    customer_return_loss=160,
    gst=13,
    ads=25
)

for k, v in result.items():
    print(f"{k}: ₹{v}")

## Small Size Should be start with Break Even Price, and add +10-20 ruppes margin