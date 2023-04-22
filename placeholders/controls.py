import os
import placeholders.tools as pt
import yaml
import warnings


warnings.filterwarnings("ignore")

def set_tags(f):
    def_file = open(f)
    definitions = yaml.safe_load(def_file)
    def_file.close()
    for file, tag in definitions.items():
        if os.path.isabs(file):
            full_path = file
        else:
            full_path = os.path.join(os.path.dirname(f), file)
        pt.set_image_tag(
            full_path,
            tag
        )    
            
    print("Complete!")
    return

def set_tag(f, t):
    pt.set_image_tag(
        f,
        t
        )
    print("Complete!")
    return

def get_tag(f):
    message = pt.get_image_tag(
        f
        )
    print(message)
    return message

def get_tags(d):
    files = os.listdir(d)
    for file in files:
        full_path = os.path.join(d, file)
        message = pt.get_image_tag(
            full_path
            )
        print(file, message)

    print("Complete!")
    return
