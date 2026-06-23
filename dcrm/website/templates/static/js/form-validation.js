/**
 * LF Carpinter CRM — Validación de formularios personalizada
 * Reemplaza los mensajes del navegador y de Django por alertas en español con diseño premium.
 */
(function () {
  'use strict';

  // ─── Mensajes por defecto en español (fallback si no hay data-msg-*) ──────────
  const DEFAULT_MSGS = {
    required:     'Este campo es obligatorio.',
    email:        'Ingresa un correo válido. Ejemplo: usuario@dominio.com',
    url:          'Ingresa una URL válida.',
    number:       'Ingresa un número válido.',
    pattern:      'El valor ingresado no tiene el formato correcto.',
    minlength:    (n) => `Mínimo ${n} caracteres.`,
    maxlength:    (n) => `Máximo ${n} caracteres.`,
    min:          (n) => `El valor mínimo es ${n}.`,
    max:          (n) => `El valor máximo es ${n}.`,
    tooShort:     (n) => `Mínimo ${n} caracteres requeridos.`,
    tooLong:      (n) => `Máximo ${n} caracteres permitidos.`,
  };

  // ─── Obtiene el mensaje correcto para cada tipo de error ──────────────────────
  function getMsg(input, validity) {
    const d = input.dataset;

    if (validity.valueMissing)
      return d.msgRequired || DEFAULT_MSGS.required;

    if (validity.typeMismatch) {
      if (input.type === 'email') return d.msgType || DEFAULT_MSGS.email;
      if (input.type === 'url')   return d.msgType || DEFAULT_MSGS.url;
      if (input.type === 'number') return d.msgType || DEFAULT_MSGS.number;
      return d.msgType || DEFAULT_MSGS.pattern;
    }

    if (validity.patternMismatch)
      return d.msgPattern || DEFAULT_MSGS.pattern;

    if (validity.tooShort)
      return d.msgMinlength || DEFAULT_MSGS.tooShort(input.minLength);

    if (validity.tooLong)
      return d.msgMaxlength || DEFAULT_MSGS.tooLong(input.maxLength);

    if (validity.rangeUnderflow)
      return d.msgMin || DEFAULT_MSGS.min(input.min);

    if (validity.rangeOverflow)
      return d.msgMax || DEFAULT_MSGS.max(input.max);

    return DEFAULT_MSGS.pattern;
  }

  // ─── Muestra un error inline bajo el input ────────────────────────────────────
  function showError(input, msg) {
    clearError(input);
    input.classList.add('input-error');

    const err = document.createElement('div');
    err.className = 'inline-error';
    err.setAttribute('role', 'alert');
    err.innerHTML =
      '<svg class="inline-error-icon" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">' +
        '<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-5a.75.75 0 01.75.75v4.5a.75.75 0 01-1.5 0v-4.5A.75.75 0 0110 5zm0 10a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd"/>' +
      '</svg>' +
      '<span>' + msg + '</span>';

    // Insertar después del input (o de su wrapper si existe)
    const wrapper = input.closest('.input-wrapper') || input;
    wrapper.insertAdjacentElement('afterend', err);
  }

  // ─── Elimina el error de un input ────────────────────────────────────────────
  function clearError(input) {
    input.classList.remove('input-error');
    const wrapper = input.closest('.input-wrapper') || input;
    const existing = wrapper.nextElementSibling;
    if (existing && existing.classList.contains('inline-error')) {
      existing.remove();
    }
  }

  // ─── Escucha el evento invalid (navegador) ───────────────────────────────────
  document.addEventListener('invalid', function (e) {
    const input = e.target;
    if (!input.validity) return;

    e.preventDefault(); // ← bloquea el globito nativo del browser

    const msg = getMsg(input, input.validity);
    input.setCustomValidity(msg);
    showError(input, msg);
  }, true);

  // ─── Limpia el error cuando el usuario empieza a corregir ────────────────────
  document.addEventListener('input', function (e) {
    const input = e.target;
    if (!input.validity) return;
    input.setCustomValidity('');
    clearError(input);
  }, true);

  // ─── Inyecta los estilos inline-error ────────────────────────────────────────
  const style = document.createElement('style');
  style.textContent = `
    .inline-error {
      display: flex;
      align-items: flex-start;
      gap: 6px;
      margin-top: 6px;
      padding: 8px 12px;
      background: rgba(239, 68, 68, 0.12);
      border: 1px solid rgba(239, 68, 68, 0.30);
      border-radius: 10px;
      color: #fca5a5;
      font-size: 0.78rem;
      font-weight: 500;
      line-height: 1.4;
      animation: slideInError 0.2s ease;
    }
    @keyframes slideInError {
      from { opacity: 0; transform: translateY(-4px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    .inline-error-icon {
      width: 14px;
      height: 14px;
      flex-shrink: 0;
      margin-top: 1px;
      color: #f87171;
    }
    .input-error, input.input-error, textarea.input-error, select.input-error, .form-control.input-error {
      border: 1px solid rgba(239, 68, 68, 0.6) !important;
      box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15) !important;
    }
  `;
  document.head.appendChild(style);

})();
