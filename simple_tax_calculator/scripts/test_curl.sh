curl -X POST "https://asia-southeast1-dataaibootcamp.cloudfunctions.net/simple_tax_calculator" \
     -H "Content-Type: application/json" \
     -d '{
         "monthly_income": 60000,
         "use_personal_allowance": true,
         "use_spouse_allowance": false,
         "num_children": 1,
         "insurance_premium": 15000,
         "social_security": 8000
     }'
