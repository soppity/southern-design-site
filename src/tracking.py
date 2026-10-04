# Google Analytics 4 measurement ID for the "Southern Design website" property
# (Analytics account "Southern Design", managed under patrick@wearelucid.uk).
# Leave empty to build the site with no analytics tag at all.
GA_MEASUREMENT_ID = "G-82G25FYWZW"


def ga_snippet(page_type):
    """The Analytics tag for one page. Advertising signals are off; this is measurement only.
    Events queue from the first moment; Google's script itself is fetched three seconds after the page has loaded
    (or at the visitor's first tap, key press or scroll, whichever comes first) so it does not slow the first paint.
    The thank-you page is the exception: it loads the script at once, so a lead is never missed."""
    if not GA_MEASUREMENT_ID:
        return ""
    return f'''
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('consent', 'default', {{ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: 'granted'}});
gtag('js', new Date());
gtag('config', '{GA_MEASUREMENT_ID}', {{content_group: '{page_type}'}});
(function(){{var done=0;function go(){{if(done)return;done=1;var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}';document.head.appendChild(s)}}
['pointerdown','keydown','touchstart','scroll'].forEach(function(e){{addEventListener(e,go,{{once:true,passive:true}})}});
if({'true' if page_type == 'Thank you' else 'false'})go();else if(document.readyState==='complete')setTimeout(go,3000);else addEventListener('load',function(){{setTimeout(go,3000)}})}})();
</script>'''
