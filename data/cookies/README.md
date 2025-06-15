
# Cookie Files Setup

To proceed with authentication or session-based access, please **save your Netscape HTTP Cookies file in this directory**.

## Required Files

- `BWT.txt`  
  Save the cookies from your browser (exported in Netscape HTTP Cookie File format) for the **BWT** service here.

## How to Export Cookies

1. Use a browser extension like **[Get cookies.txt](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)**.
2. Log in to the target website in your browser.
3. Click the extension icon and export the cookies.
4. Save the file as `BWT.txt` in this directory.

> ⚠️ Make sure the file is in the **Netscape HTTP Cookie File format**, or it will not work.

---

## Example Cookie Format (`BWT.txt`)

```
# Netscape HTTP Cookie File
# http://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file!  Do not edit.

bwtorrents.tv	FALSE	/	FALSE	xxxxx	uid	xxxxx
bwtorrents.tv	FALSE	/	FALSE	xxxxx	pass	xxxxx
```

> Replace `uid` and `pass` values with the ones from your actual login session.
