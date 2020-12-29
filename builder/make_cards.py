from bs4 import BeautifulSoup
import sys
import yaml
import os
from style import style as colours

SOURCE, OUTPUT = sys.argv[1], sys.argv[2]

ESCDICT = {
        "&" : "&amp;",
        "<" : "&lt;",
        ">" : "&gt;",
        '"' : "&quot;",
        "'" : "&#x27;",
        "`" : "&#x60;",
        "=" : "&#x3D;",
        "\n" : "<br>"}

ESCCHARS = ESCDICT.keys()

# default indent at 4 spaces.
INDENT = "    "

def esc(string):
    """
    Escapes special characters for use in HTML:
    & < > " ' ` =
    n.b. creates new string rather than modifying in place.
    Note that for card text layout purposes, this also replaces newlines with
    <br>.
    """
    out = ""
    for char in string:
        if char in ESCCHARS:
            out += ESCDICT[char]
        else:
            out += char
    return out

def nip(string):
    """
    Rather than escaping special chars like above, this simply deletes them.
    For use in CSS classes and other restrictive environments.
    N.B. THIS ALSO PUTS EVERYTHING IN LOWERCASE FOR CONSISTENCY
    """
    out = ""
    for char in string.lower():
        if char.isalnum() or char in  "_-":
            out += char
    if out == "":
        out = "BADSTRING"
    return out

def dict_to_html(card, category, colour):
    """
    Converts one list entry from a YAML file into an HTML card for use
    in index.html.
    
    Takes as input a category, which will ba added to the tags.
    
    Also takes in a Materialize.css colour as input, in the form of a string.
    
    Local variables defined from card:
    - title
    - image
    - content
    - locations
    - links
    """
    ck = card.keys()
    
    # get important values from card dict
    if "title" in ck and isinstance(card["title"], str):
        title = card["title"]
    else:
        title = None
    
    if "image" in ck and isinstance(card["image"], str):
        image = card["image"]
    else:
        image = None
    
    if "content" in ck and isinstance(card["content"], str):
        content = card["content"]
    else:
        content = None
    
    locations = []
    if "locations" in ck and isinstance(card["locations"], list):
        for location in card["locations"]:
            if isinstance(location, str):
                locations.append(location)
    
    links = []
    if "links" in ck and isinstance(card["links"], list):
        for link in card["links"]:
            if isinstance(link, dict) and "url" in link.keys() and "text" in link.keys():
                links.append((link["url"], link["text"]))
    
    # START CREATING OUTPUT.
    
    # Initialise div and CSS classes
    out = ("<div class=\"card " # create css for card
          + colour + " lighten-2 " # define colour
          + "cat-" + nip(category)) # add category tag
    # Add geo filters
    for location in locations:
        out += " geo-" + nip(location)
    # Close CSS
    out += '"'
    # Add data-name. Contingency for if undefined title.
    if title:
        out += " data-name=\"" + esc(title) + "\">"
    else:
        out += " data-name=\"Image\">"
    
    # Add image div, if there is an image.
    if image:
        out += "\n\n" + INDENT
        out += "<div class=\"card-image\">"
        out += "\n" + 2 * INDENT
        out += "<img src=\"img/cards/" + image + "\">"
        
        # Add title on top of image if necessary.
        if title:
            out += "\n" + 2 * INDENT
            out += "<span class=\"card-title " + colour + "-text"
            out += " text-darken-4\">"
            out += esc(title)
            out += "</span>"
        
        out += "\n" + INDENT
        out += "</div>"
    
    # Add the bulk of the card, if there is a reason to (there should be).
    if title or content:
        out += "\n\n" + INDENT
        out += "<div class=\"card-content\">"
        out += "\n"
        
        # only add a title here if it wasn't added on the image.
        if title and not image:
            out += 2 * INDENT
            out += "<span class=\"card-title "
            out += colour + "-text text-darken-4\">"
            out += esc(title)
            out += "</span>"
            out += "\n"
            
        if content:
            out += 2 * INDENT
            out += "<p class=\"black-text text-darken-4\">"
            out += esc(content)
            out += "</p>"
            out += "\n"
        
        out += INDENT + "</div>"
    
    # add the links at bottom of card.
    if links:
        out += "\n\n" + INDENT
        out += "<div class=\"card-action\">"
        count = 0
        for link in links:
            count += 1
            out += "\n" + 2 * INDENT
            out += "<a href=\"" + link[0] + "\">"
            out += "\n" + 3 * INDENT
            out += "<span class=\"" + colour + "-text text-darken-4\">"
            out += esc(link[1])
            out += "</span>"
            out += "\n" + 2 * INDENT
            out += "</a>"
            if count < len(links):
                out += "<br>"
        out += "\n" + INDENT
        out += "</div>"
    
    # add locations at bottom of card.
    if locations:
        out += "\n\n" + INDENT
        out += "<div class=\"beans\">"
        for loc in locations:
            out += "\n" + 2 * INDENT
            out += "<div class=\"bean " + colour + " darken-4 "
            out += colour + "-text text-lighten-3\">"
            out += "\n" + 3 * INDENT
            out += loc
            out += "\n" + 2 * INDENT
            out += "</div>"
        out += "\n" + INDENT
        out += "</div>"
    
    out += "\n"
    out += "</div>"
    
    return out

def catset_to_dropdown(cat_set):
    """
    Another helper function which turns a set of category tuples into a
    dropdown.
    
    Each category that is not "all" has a circular icon on the side with the
    corresponding card colour.
    """
    # Initialise the ul
    out = "<ul class=\"dropdown-content slid-cat-dropdown\" id=\"dropdown-cat\">\n"
    # Add the "all" filter by default
    out += "<li class=\"active\">\n<a class=\"slid-filter\" filter=\"\" slid-group=\"cat\">All</a>\n</li>\n"
    
    cat_list = list(cat_set)
    # Make alphabetical by category
    cat_list.sort()
    
    for tup in cat_list:
        out += "<li>\n"
        out += "<a class=\"slid-filter\" filter=\".cat-"
        out += nip(tup[0])
        out += "\" slid-group=\"cat\">"
        out += "<i class=\"material-icons left "
        out += tup[1]
        out += "-text text-lighten-1\">brightness_1</i>"
        out += esc(tup[0])
        out += "</a>\n</li>\n"
    
    # Close the ul
    out += "</ul>"
    return out

def geoset_to_dropdown(geo_set):
    """
    Just like the catset function, but doesn't make colourful icons.
    """
    # Initialise the ul
    out = "<ul class=\"dropdown-content slid-geo-dropdown\" id=\"dropdown-geo\">\n"
    # Add the "all" filter by default
    out += "<li class=\"active\">\n<a class=\"slid-filter\" filter=\"\" slid-group=\"geo\">All</a>\n</li>\n"
    
    geo_list = list(geo_set)
    # Make alph
    geo_list.sort()
    
    for loc in geo_list:
        out += "<li>\n"
        out += "<a class=\"slid-filter\" filter=\".geo-"
        out += nip(loc)
        out += "\" slid-group=\"geo\">"
        out += esc(loc)
        out += "</a>\n</li>\n"
    
    # Close the ul
    out += "</ul>"
    return out

# We're going to run through every yml file and create a new string containins
# all cards to go in the grid. Initialise this string with the enclosing div 
# tag.
newgridstring = "<div class=\"grid\">\n"

# Also initialise a set of category tags and a list of location tags.
# The category set contains tuples (category, colour).
cat_set = set()
geo_set = set()

for filename in os.listdir(SOURCE):
    if filename.endswith(".yml") or filename.endswith(".yaml"):

        sourcefile = os.path.join(SOURCE, filename)
        # The category is the filename with no extension.
        cat = ".".join(filename.split(".")[:-1])

        with open(sourcefile, "r") as file:

            content = yaml.load(file, Loader=yaml.FullLoader)
            
            if cat in colours.keys():
                colour = colours[cat]
            else:
                colour = "yellow"
            
            cat_set.add((cat, colour))

            for card in content:
                newgridstring += dict_to_html(card, cat, colour)
                newgridstring += "\n"
                
                # Add all geo filters
                if "locations" in card.keys():
                    for location in card["locations"]:
                        if isinstance(location, str):
                            geo_set.add(location)

# We have now added all cards to the new string; close the div tag
newgridstring += "</div>"

# Now load and read the output file with bs4
with open(OUTPUT, "r") as file:
    soup = BeautifulSoup(file, "html.parser")


# FIRST STEP: generate cards
def isgrid(tag):
    return tag.has_attr("class") and 'grid' in tag["class"]
grid = soup.find(isgrid)
newgrid = BeautifulSoup(newgridstring, "html.parser")
grid.replace_with(newgrid)

# SECOND STEP: generate category filter dropdown
cat_dropdown = soup.find(id="dropdown-cat")
new_cat_dropdown = BeautifulSoup(catset_to_dropdown(cat_set), "html.parser")
cat_dropdown.replace_with(new_cat_dropdown)

# THIRD STEP: generate location filter dropdown
geo_dropdown = soup.find(id="dropdown-geo")
new_geo_dropdown = BeautifulSoup(geoset_to_dropdown(geo_set), "html.parser")
geo_dropdown.replace_with(new_geo_dropdown)

# Now pretty-print the file and save
out = soup.prettify()
with open(OUTPUT, "w") as file:
    file.write(out)
