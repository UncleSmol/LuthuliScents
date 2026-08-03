"""Scroll helper: jump the app back to the top when switching views.

Streamlit keeps the main container's scroll position across re-runs, so a
plain script injected per navigation never re-runs (the injected iframe is
only freshly created once). Instead we install a single observer on first
load that watches a marker div (updated from Python with the current page)
and scrolls to the top only when the page changes.
"""

import streamlit as st

_OBSERVER = """
<script>
(function () {
    var win = window.parent;
    var last = null;
    function scrollTop() {
        var targets = win.document.querySelectorAll(
            '[data-testid="stMain"], [data-testid="stAppViewContainer"], [data-testid="stApp"]'
        );
        for (var i = 0; i < targets.length; i++) targets[i].scrollTop = 0;
        win.scrollTo(0, 0);
    }
    function check() {
        var el = win.document.getElementById('ls-page');
        if (!el) return;
        var page = el.getAttribute('data-page');
        if (last !== null && last !== page) {
            var tries = 0;
            var timer = setInterval(function () {
                scrollTop();
                if (++tries > 15) clearInterval(timer);
            }, 100);
        }
        last = page;
    }
    check();
    var observer = new win.MutationObserver(check);
    observer.observe(win.document.documentElement, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['data-page'],
    });
    var timer = setInterval(check, 800);
})();
</script>
"""


def install_scroll_observer() -> None:
    st.components.v1.html(_OBSERVER, height=0)


def mark_page(page: str) -> None:
    st.markdown(
        f'<div id="ls-page" data-page="{page}" style="display:none"></div>',
        unsafe_allow_html=True,
    )
