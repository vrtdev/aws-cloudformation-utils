def r53_hosted_zone_id():
    """
    Return a mapping of (region, service) -> hosted zone id
    """
    input_map = {
        'ElasticBeanstalk': {
            'us-east-1': 'Z117KPS5GTRQ2G',
            'us-west-1': 'Z1LQECGX5PH1X',
            'us-west-2': 'Z38NKT9BP95V3O',
            'ap-south-1': 'Z18NTBI3Y7N9TZ',
            'ap-northeast-2': 'Z3JE5OI70TWKCP',
            'ap-southeast-1': 'Z16FZ9L249IFLT',
            'ap-southeast-2': 'Z2PCDNR3VC2G1N',
            'ap-northeast-1': 'Z1R25G3KIG2GBW',
            'eu-central-1': 'Z1FRNW7UH4DEZJ',
            'eu-west-1': 'Z2NYPWQ7DFZAZH',
            'sa-east-1': 'Z10X7K2B4QSOFV',
        },
        'ElasticLoadBalancing': {
            'us-east-1': 'Z35SXDOTRQ7X7K',
            'us-west-1': 'Z368ELLRRE2KJ0',
            'us-west-2': 'Z1H1FL5HABSF5',
            'ap-south-1': 'ZP97RAFLXTNZK',
            'ap-northeast-2': 'ZWKZPGTI48KDX',
            'ap-southeast-1': 'Z1LMS91P8CMLE5',
            'ap-southeast-2': 'Z1GM3OXH4ZPM65',
            'ap-northeast-1': 'Z14GRHDCWA56QT',
            'eu-central-1': 'Z215JYRZR1TBD5',
            'eu-west-1': 'Z32O12XQLNTSW2',
            'sa-east-1': 'Z2P70J7HTTTPLU',
        },
        'CloudFront': {
            '_default': 'Z2FDTNDATAQYW2',  # Cloudfront has only one hosted zone id (global service)
        },
        'APIGateway': {
            'us-east-2': 'ZOJJZC49E0EPZ',
            'us-east-1': 'Z1UJRXOUMOOFQ8',
            'us-west-1': 'Z2MUQ32089INYE',
            'us-west-2': 'Z2OJLYMUO9EFXC',
            'ap-south-1': 'Z3VO1THU9YC4UR',
            'ap-northeast-3': 'Z2YQB5RD63NC85',
            'ap-northeast-2': 'Z20JF4UZKIW1U8',
            'ap-southeast-1': 'ZL327KTPIQFUL',
            'ap-southeast-2': 'Z2RPCDW04V8134',
            'ap-northeast-1': 'Z1YSHQZHG15GKL',
            'ca-central-1': 'Z19DQILCV0OWEC',
            'eu-central-1': 'Z1U9ULNL0V5AJ3',
            'eu-west-1': 'ZLY8HYME6SFDD',
            'eu-west-2': 'ZJ5UAJN8Y3Z2Q',
            'eu-west-3': 'Z3KY65QIEKYHQQ',
            'eu-north-1': 'Z2YB950C88HT6D',
            'sa-east-1': 'ZCMLWB8V5SYIT',
        },
    }

    # Aggregate all listed regions
    regions = set()
    for region_map in input_map.values():
        regions.update(region_map.keys())
    regions.discard('_default')

    output = {}
    for region in regions:
        for service in input_map:
            try:
                hosted_zone_id = input_map[service][region]
            except KeyError:
                hosted_zone_id = input_map[service]['_default']

            if region not in output:
                output[region] = {}
            output[region][service] = hosted_zone_id

    return output
