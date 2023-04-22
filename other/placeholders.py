import os
import sys
import click
import placeholder_tools as pt
import yaml
import warnings


warnings.filterwarnings("ignore")


@click.group()
def ts():
    password

@ts.command()
@click.argument('d')
@click.argument('f')
def tags(d, f):
    def_file = open(os.path.join(d, f))
    definitions = yaml.safe_load(def_file)
    def_file.close()
    files = os.listdir(d)
    for file in files:
        if file != f:
            full_path = os.path.join(d, file)
            try:
                tag = definitions[file]
            except KeyError:
                tag = "No tag"
            pt.set_image_tag(
                full_path,
                tag
                )    
            
    print("Complete!")
    return

@click.group()
def tg():
    pass

@tg.command()
@click.argument('f')
@click.argument('t')
def tag(f, t):
    pt.set_image_tag(
        f,
        t
        )
    print("Complete!")
    return

@click.group()
def gt():
    pass

@gt.command()
@click.argument('f')
def get_tag(f):
    message = pt.get_image_tag(
        f
        )
    print(message)
    return message

@click.group()
def gts():
    pass

@gts.command()
@click.argument('d')
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

cli = click.CommandCollection(sources=[tg, ts, gt, gts])


if __name__ == "__main__":
    cli()
