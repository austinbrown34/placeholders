from pdfminer.pdftypes import LITERALS_DCT_DECODE
from pdfminer.pdfcolor import LITERAL_DEVICE_GRAY
from pdfminer.pdfcolor import LITERAL_DEVICE_RGB
import boto3
import os
import yaml
from shutil import copyfile
import requests
import json
import tools
import config


class TemplateService(object):
    def __init__(self, directory):
        self.directory = directory

    def download_config(self, config_folder, myconfig, destination):
        try:
            copyfile(os.path.join(self.directory, config_folder, myconfig), destination)
        except Exception as e:
            tools.pretty_print(
                'Download Config Exception: {}\nIssue with downloading config.yaml'.format(e), 'fail')


    def get_templates(self, myconfig, template_folder, template_keys):
        templates = []
        def template_list_builder(temp_templates):
            for temp in temp_templates:
                if not isinstance(temp, (str, unicode)):
                    template_list_builder(temp)
                    continue
                templates.append(temp)
        try:
            cfg = open(myconfig)
            cfg_obj = yaml.safe_load(cfg)
            cfg.close()
            logo = cfg_obj[config.TEMPLATE_LOGO_KEYWORD]
            user = cfg_obj.get(config.TEMPLATE_USER_KEYWORD, config.NO_TEMPLATE_USER_KEYWORD)
            temp_templates = []
            template_rules = cfg_obj[config.TEMPLATE_RULES_KEYWORD]
            unmatched = []
            for i, rule in enumerate(template_rules):
                matched = False
                for j, template_key in enumerate(template_keys):
                    try:
                        template_key[0] = template_key[0].replace(u'\u2013', '-')
                    except Exception as e:
                        pass
                    try:
                        template_key[1] = template_key[1].replace(u'\u2013', '-')
                    except Exception as e:
                        pass
                    tools.pretty_print(rule[config.TEMPLATE_RULE_KEYWORD][config.TEMPLATE_PACKAGE_NAME_KEYWORD])
                    tools.pretty_print(template_key[1])
                    if rule[config.TEMPLATE_RULE_KEYWORD][config.TEMPLATE_PACKAGE_KEY_KEYWORD] is not None:
                        if template_key[0] == rule[config.TEMPLATE_RULE_KEYWORD][config.TEMPLATE_PACKAGE_KEY_KEYWORD]:
                            temp_templates.append(rule[config.TEMPLATE_RULE_KEYWORD][config.TEMPLATE_INCLUDED_TEMPLATES_KEYWORD])
                            matched = True
                    else:
                        if template_key[1] == rule[config.TEMPLATE_RULE_KEYWORD][config.TEMPLATE_PACKAGE_NAME_KEYWORD]:
                            temp_templates.append(rule[config.TEMPLATE_RULE_KEYWORD][config.TEMPLATE_INCLUDED_TEMPLATES_KEYWORD])
                            matched = True
                    if not matched:
                        unmatched.append({
                            'template_key': template_key[0],
                            'template_name': template_key[1],
                        })
            message = 'The following packages for {} are missing templates: \n\n'.format(user)
            for i, e in enumerate(unmatched):
                message += 'PKG NAME: {}\nPKG KEY: {}\n\n'.format(e['template_name'], e['template_key'])
            if len(unmatched) > 0:
                tools.pretty_print(message, 'fail')
            template_list_builder(temp_templates)
        except Exception as e:
            tools.pretty_print(
                'Get Templates Exception: {}\nIssue with parsing config.yaml...'.format(e), 'fail')
            pass
        return templates

    def get_logo(self, myconfig):
        logo = ''
        try:
            cfg = open(myconfig)
            cfg_obj = yaml.safe_load(cfg)
            cfg.close()
            logo = cfg_obj[config.TEMPLATE_LOGO_KEYWORD]
        except Exception as e:
            tools.pretty_print(
                'Get Logo Exception: {}\nIssue parsing logo from config.yaml...'.format(e), 'fail')
            pass
        return logo

    def get_scripts(self, myconfig):
        scripts = []
        try:
            cfg = open(myconfig)
            cfg_obj = yaml.safe_load(cfg)
            cfg.close()
            if cfg_obj is not None:
                template_scripts = cfg_obj[config.TEMPLATE_SCRIPTS_KEYWORD]
            if template_scripts is None:
                scripts = []
            else:
                for script in template_scripts:
                    scripts.append(script)
        except Exception as e:
            tools.pretty_print(
                'Get Scripts Exception: {}\nIssue with parsing scripts from config.yaml...'.format(e), 'fail')
            pass
        return scripts

    def download_templates(self, template_folder, templates):
        for template in templates:
            try:
                copyfile(
                    os.path.join(
                        self.directory,
                        template_folder,
                        template
                        ),
                    os.path.join(
                        config.BASE_FOLDER,
                        config.WORK_FOLDER_NAME,
                        template
                        )
                    )
            except Exception as e:
                tools.pretty_print('Download Templates Exception: {}\nIssue downloading templates...'.format(e), 'fail')
                pass

    def download_scripts(self, template_folder, scripts):
        for script in scripts:
            try:
                copyfile(
                    os.path.join(
                        self.directory,
                        template_folder,
                        script
                        ),
                    os.path.join(
                        config.BASE_FOLDER,
                        config.WORK_FOLDER_NAME,
                        script
                        )
                    )
                tools.pretty_print('Downloaded Scripts...')
            except Exception as e:
                tools.pretty_print('Download Scripts Exception: {}\nIssue downloading scripts...'.format(e), 'fail')
                pass


class S3TemplateService(object):

    def __init__(self, credentials=None, bucket=None):
        if credentials is None:
            self.credentials = None
        else:
            self.credentials = credentials
        if bucket is None:
            return
        self.bucket = bucket
        if self.credentials is not None:
            self.session = boto3.Session(
                aws_access_key_id=credentials['aws_access_key_id'],
                aws_secret_access_key=credentials['aws_secret_access_key']
            )
        else:
            self.session = boto3.Session()
        self.s3 = self.session.resource('s3')
        self.s3_client = self.session.client('s3')


    def download_config(self, config_folder, myconfig, destination):
        def lambda_handler(event, context):
            bucket_name = event['Records'][0]['s3']['bucket']['name']
            key = event['Records'][0]['s3']['object']['key']
            if not key.endswith('/'):
                try:
                    split_key = key.split('/')
                    file_name = split_key[-1]
                    s3templates.s3.meta.client.download_file(
                        bucket_name,
                        key,
                        os.path.join(config.WORK_FOLDER, config.TEMPLATE_CONFIG_FILE)
                        )
                except Exception as e:
                    tools.pretty_print('Download Config Lambda Handler Exception: {}'.format(e), 'fail')
            return (bucket_name, key)
        try:
            tools.pretty_print('Trying to download config with this info: \nbucket: {}\npath: {}\ndestination: {}'.format(
                self.bucket,
                os.path.join(config_folder, myconfig),
                destination
            ))
            self.s3.meta.client.download_file(
                self.bucket,
                os.path.join(config_folder, myconfig),
                destination
                )
        except Exception as e:
            tools.pretty_print('Download Config Exception: {}'.format(e), 'fail')


    def get_templates(self, myconfig, template_folder, template_keys):
        templates = []
        def template_list_builder(temp_templates):
            for temp in temp_templates:
                if not isinstance(temp, (str, unicode)):
                    template_list_builder(temp)
                    continue
                templates.append(temp)
        try:
            cfg = open(myconfig)
            cfg_obj = yaml.safe_load(cfg)
            cfg.close()
            temp_templates = []
            template_rules = cfg_obj[config.TEMPLATE_RULES_KEYWORD]
            logo = cfg_obj[config.TEMPLATE_LOGO_KEYWORD]
            user = cfg_obj.get(config.TEMPLATE_USER_KEYWORD, config.NO_TEMPLATE_USER_KEYWORD)
            unmatched = []
            for i, rule in enumerate(template_rules):
                matched = False
                if rule[config.TEMPLATE_RULE_KEYWORD][config.TEMPLATE_INCLUDED_TEMPLATES_KEYWORD] is not None:
                    for j, template_key in enumerate(template_keys):
                        try:
                            template_key[0] = template_key[0].replace(u'\u2013', '-')
                        except Exception as e:
                            pass
                        try:
                            template_key[1] = template_key[1].replace(u'\u2013', '-')
                        except Exception as e:
                            pass
                        if config.TEMPLATE_INTERNAL_ID_KEYWORD in rule[config.TEMPLATE_RULE_KEYWORD]:
                            if template_key[2] == rule[config.TEMPLATE_RULE_KEYWORD][config.TEMPLATE_INTERNAL_ID_KEYWORD]:
                                temp_templates.append(rule[config.TEMPLATE_RULE_KEYWORD][config.TEMPLATE_INTERNAL_ID_KEYWORD])
                                matched = True
                        if config.TEMPLATE_PACKAGE_KEY_KEYWORD in rule[config.TEMPLATE_RULE_KEYWORD]:
                            if rule[config.TEMPLATE_RULE_KEYWORD][config.TEMPLATE_PACKAGE_KEY_KEYWORD] is not None and not matched:
                                if template_key[0] == rule[config.TEMPLATE_RULE_KEYWORD][config.TEMPLATE_PACKAGE_KEY_KEYWORD] or str(template_key[2]) == rule[config.TEMPLATE_RULE_KEYWORD][config.TEMPLATE_PACKAGE_KEY_KEYWORD]:
                                    temp_templates.append(rule[config.TEMPLATE_RULE_KEYWORD][config.TEMPLATE_INCLUDED_TEMPLATES_KEYWORD])
                                    matched = True
                        if not matched:
                            if template_key[1] == rule[config.TEMPLATE_RULE_KEYWORD][config.TEMPLATE_PACKAGE_NAME_KEYWORD]:
                                temp_templates.append(rule[config.TEMPLATE_RULE_KEYWORD][config.TEMPLATE_INCLUDED_TEMPLATES_KEYWORD])
                                matched = True
                        if not matched:
                            unmatched.append({
                                'template_key': template_key[0],
                                'template_name': template_key[1],
                            })
            message = 'The following packages for {} ar missing templates: \n\n'.format(user)
            for i, e in enumerate(unmatched):
                message += 'PKG NAME: {}\nPKG KEY: {}\n\n'.format(e['template_name'], e['template_key'])
            if len(unmatched) > 0:
                tools.pretty_print(message, 'fail')
            template_list_builder(temp_templates)
        except Exception as e:
            tools.pretty_print('Get Templates Exception: {}\nIssue with parsing config.yaml...'.format(e), 'fail')
            pass
        return templates

    def get_logo(self, myconfig):
        logo = ''
        try:
            cfg = open(myconfig)
            cfg_obj = yaml.safe_load(cfg)
            cfg.close()
            logo = cfg_obj[config.TEMPLATE_LOGO_KEYWORD]
        except Exception as e:
            tools.pretty_print('Get Logo Exception: {}\nIssue parsing logo from config.yaml...'.format(e), 'fail')
            pass
        return logo
    def get_scripts(self, myconfig):
        scripts = []
        try:
            cfg = open(myconfig)
            cfg_obj = yaml.safe_load(cfg)
            cfg.close()
            if cfg_obj is not None:
                template_scripts = cfg_obj[config.TEMPLATE_SCRIPTS_KEYWORD]
                if template_scripts is None:
                    scripts = []
                else:
                    for script in template_scripts:
                        scripts.append(script)
        except Exception as e:
            tools.pretty_print('Get Scripts Exception: {}\nIssue with parsing scripts from config.yaml...'.format(e), 'fail')
            pass
        return scripts

    def download_templates(self, template_folder, templates):
        for template in templates:
            def lambda_handler(event, context):
                bucket_name = event['Records'][0]['s3']['bucket']['name']
                key = event['Records'][0]['s3']['object']['key']
                if not key.endswith('/'):
                    try:
                        split_key = key.split('/')
                        file_name = split_key[-1]
                        s3templates.s3.meta.client.download_file(
                            bucket_name,
                            key,
                            os.path.join(config.WORK_FOLDER, template)
                            )
                    except Exception as e:
                        tools.pretty_print('Download Templates Lambda Handler Exception: {}'.format(e), 'fail')
                return (bucket_name, key)
            try:
                self.s3.meta.client.download_file(
                    self.bucket,
                    os.path.join(template_folder, template),
                    os.path.join(config.BASE_FOLDER, config.WORK_FOLDER_NAME, template)
                )
            except Exception as e:
                tools.pretty_print('Download Templates Exception: {}\nIssue with downloading templates...'.format(e), 'fail')
                pass

    def download_scripts(self, template_folder, scripts):
        for script in scripts:
            def lambda_handler(event, context):
                bucket_name = event['Records'][0]['s3']['bucket']['name']
                key = event['Records'][0]['s3']['object']['key']
                if not key.endswith('/'):
                    try:
                        split_key = key.split('/')
                        file_name = split_key[-1]
                        s3templates.s3.meta.client.download_file(
                            bucket_name,
                            key,
                            os.path.join(config.WORK_FOLDER, script)
                        )
                    except Exception as e:
                        tools.pretty_print('Download Scripts Lambda Handler Exception: {}'.format(e), 'fail')
                return (bucket_name, key)
            try:
                self.s3.meta.client.download_file(
                    self.bucket,
                    os.path.join(template_folder, script),
                    os.path.join(config.BASE_FOLDER, config.WORK_FOLDER_NAME, script)
                )
                tools.pretty_print('Downloaded Scripts...')
            except Exception as e:
                tools.pretty_print('Download Scripts Exception: {}\nIssue with downloading scripts...'.format(e), 'fail')
                pass

    def get_presigned_url(self, pdf):
        presigned_url = ''
        try:
            presigned_url = self.s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': self.Bucket,
                    'Key': pdf
                }
            )
        except Exception as e:
            tools.pretty_print('Get Presigned URL Exception: {}\nIssue generating presigned URL...'.format(e), 'fail')
            pass
        return presigned_url


class ImageExtractorService(object):

    def __init__(self, outdir):
        self.outdir = outdir
        self.jpgs = []
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)
        return

    def get_jpgs(self):
        return self.jpgs

    def export_image(self, image):
        stream = image.stream
        filters = stream.get_filters()
        (width, height) = image.srcsize
        if len(filters) == 1 and filters[0] in LITERALS_DCT_DECODE:
            ext = '.jpg'
            name = image.name + ext
            path = os.path.join(self.outdir, name)
            fp = file(path, 'wb')
            raw_data = stream.get_rawdata()
            fp.write(raw_data)
            fp.close()
            self.jpgs.append(image.name + ext)
        elif (image.bits == 1 or
              image.bits == 8 and
              image.colorspace in (LITERAL_DEVICE_RGB, LITERAL_DEVICE_GRAY)):
            ext = config.BMP_FILE_PATTERN % (width, height)
        else:
            ext = config.IMG_FILE_PATTERN % (image.bits, width, height)
        name = image.name + ext
        return name
