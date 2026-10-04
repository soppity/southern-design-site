# Google Analytics 4 measurement ID for the "Southern Design website" property
# (Analytics account "Southern Design", managed under patrick@wearelucid.uk).
# Leave empty to build the site with no analytics tag at all.
GA_MEASUREMENT_ID = "G-82G25FYWZW"


def ga_snippet(page_type):
    """The Analytics tag for one page. Advertising signals are off; this is measurement only."""
    if not GA_MEASUREMENT_ID:
        return ""
    return f'''
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('consent', 'default', {{ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: 'granted'}});
gtag('js', new Date());
gtag('config', '{GA_MEASUREMENT_ID}', {{content_group: '{page_type}'}});
</script>'''
