
import os

def spacify(_string):
    return _string.replace("-", " ")

directory = "static/img"
server_name = "gifs.b17.dev"
images = []
for (root,dirs,files) in os.walk("static/img"):
    for f in files:
        name,ext = os.path.splitext(f)

        if ext in [".jpg", ".png", ".gif", ".webp"]:
            images.append(("/{directory}/{file}".format(directory=directory, file=f), name))

images.sort(key=lambda x: x[1])

s = """
foreach ($scanned_directory as $value)
{
    preg_match('/([^.]+).(jpg|png|gif)/', $value, $matches, PREG_OFFSET_CAPTURE);
    if (count($matches) > 0)
    {
        array_push($images, array("/$directory/$value", $matches[1][0]));
    }
}

?>
"""
header = """<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="/static/css/main.css" />
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.4.2/css/all.css" crossorigin="anonymous"/>

    <title>{title}</title>

<script>
function copyToClipboard(address)
{{
    const _textarea = document.createElement('textarea')
    _textarea.value = window.location.origin + address;

    // make it hidden
    _textarea.setAttribute('readonly', '');
    _textarea.style.position = 'fixed';
    _textarea.style.left = 0;
    _textarea.style.top = 0;
    _textarea.style.width = '2em';
    _textarea.style.height = '2em';
    _textarea.style.padding = 0;
    _textarea.style.border = 'none';
    _textarea.style.outline = 'none';
    _textarea.style.boxShadow = 'none';
    _textarea.style.background = 'transparent';

    // add the element
    document.body.appendChild(_textarea);

    // select the text
    _textarea.focus();
    _textarea.select();
    /*
    var sel = getSelection();
    var range = document.createRange();
    range.selectNode(_textarea);
    sel.removeAllRanges();
    sel.addRange(range);
    */
    if (document.execCommand('copy'))
    {{
        console.log("copied text: " + _textarea.value);
    }}
    document.body.removeChild(_textarea);
}}

</script>
  </head>
""".format(title=server_name)

body = """
    <body class="bg-indigo-lightest font-sans">
        <input id="image-address" type="text" readonly="readonly" class="hidden"
                value="https://{server}{first}" />
        <div class="grid max-w-4xl mx-auto p-8">
""".format(server=server_name, first=images[0][0])

footer = """
        </div>
    </div>
  </body>
</html>
</head>
"""

img = """
    <a href='#' class='bg-white rounded h-full text-grey-darkest no-underline shadow-md'
        onClick="copyToClipboard('{path}');return false;">
        <h1 class="text-3xl p-6">{name}</h1>
        <img class="w-full block rounded-b" src="{path}">
    </a>
"""
with open("index.html", "w") as f:
    f.write(header)
    f.write(body)


    for value in images:
        f.write(img.format(path=value[0], name=value[1]))

    f.write(footer)

