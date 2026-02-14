export const salaryFormatter = (value: number) => new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "DOP", 
}).format(value)