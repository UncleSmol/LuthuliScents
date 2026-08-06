/* LuthuliScents — contact page: build a pre-filled WhatsApp enquiry link. */

(function () {
  'use strict';

  var WHATSAPP_NUMBER = '27692380796';

  function initContactForm() {
    var form = document.getElementById('contact-form');
    if (!form) return;

    var resultEl = document.getElementById('contact-result');

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      var name = (form.elements.name ? form.elements.name.value : '').trim();
      var message = (form.elements.message ? form.elements.message.value : '').trim();
      if (!name || !message) {
        resultEl.innerHTML = '<div class="alert warning">Please add your name and a message.</div>';
        return;
      }
      var email = (form.elements.email ? form.elements.email.value : '').trim();
      var phone = (form.elements.phone ? form.elements.phone.value : '').trim();
      var subject = (form.elements.subject ? form.elements.subject.value : '').trim();

      var text =
        'Hi LuthuliScents! My name is ' + name + '.\n' +
        'Subject: ' + subject + '\n' +
        'Message: ' + message +
        (email ? '\nContact: ' + email : '') +
        (phone ? ' / ' + phone : '');

      resultEl.innerHTML =
        '<div class="alert success">Your message is ready to send.' +
        ' <a class="btn primary" style="margin-left:8px;" href="https://wa.me/' + WHATSAPP_NUMBER + '?text=' +
        encodeURIComponent(text) + '" target="_blank" rel="noopener">Open WhatsApp</a></div>';
    });
  }

  initContactForm();
})();