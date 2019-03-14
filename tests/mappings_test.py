import cfnutils.mappings


def test_hosted_zone_id():
    mapping = cfnutils.mappings.r53_hosted_zone_id()
    # this will raise if not all regions are filled in

    assert len(mapping) > 0
    for region, regional_mapping in mapping.items():
        assert len(regional_mapping) > 0

    # take a few samples
    assert 'Z2FDTNDATAQYW2' == mapping['eu-west-1']['CloudFront']
    assert 'Z1H1FL5HABSF5' == mapping['us-west-2']['ElasticLoadBalancing']
    assert 'Z3VO1THU9YC4UR' == mapping['ap-south-1']['APIGateway']
