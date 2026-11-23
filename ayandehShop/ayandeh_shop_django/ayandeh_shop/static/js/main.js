// فایل آماده توسعه تعاملات سمت کاربر در آینده شاپ
document.addEventListener("DOMContentLoaded", () => {
  // اعتبارسنجی سمت مرورگر صرفاً برای تجربه کاربری است؛
  // اعتبارسنجی نهایی همیشه باید در Django انجام شود.
  document.querySelectorAll("input[type='number'][name='quantity']").forEach((input) => {
    input.addEventListener("change", () => {
      const min = Number(input.min || 1);
      const max = Number(input.max || 999);
      let value = Number(input.value || min);
      input.value = Math.min(Math.max(value, min), max);
    });
  });
});
