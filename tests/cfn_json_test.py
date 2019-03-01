from troposphere import Sub, Ref

from cfnutils.cfn_json import cfn_json_dumps


def test_normal():
    assert cfn_json_dumps("foo") == '"foo"'
    assert cfn_json_dumps(True) == 'true'
    assert cfn_json_dumps(42) == '42'
    assert cfn_json_dumps({'foo': 'bar'}) == '{"foo": "bar"}'
    assert cfn_json_dumps(['foo', 'bar']) == '["foo", "bar"]'
    assert cfn_json_dumps({'foo': ['bar', 42, True]}) == '{"foo": ["bar", 42, true]}'
    assert cfn_json_dumps(None) == "null"


def test_sub():
    data_in = Sub("test")
    data_out = cfn_json_dumps(data_in)
    assert isinstance(data_out, Sub)
    assert data_out.data == {'Fn::Sub': ['"${Sub_0}"', {"Sub_0": data_in}]}


def test_multi_sub():
    data_in = [Sub("test"), Sub("test2")]
    data_out = cfn_json_dumps(data_in)
    assert isinstance(data_out, Sub)
    assert data_out.data == {'Fn::Sub': ['["${Sub_0}", "${Sub_1}"]',
                                         {"Sub_0": data_in[0],
                                          "Sub_1": data_in[1],
                                          }]}


def test_multi_sub_ref():
    data_in = [Sub("test"), Ref("foo"), Sub("test2")]
    data_out = cfn_json_dumps(data_in)
    assert isinstance(data_out, Sub)
    assert data_out.data == {'Fn::Sub': [
        '["${Sub_0}", "${Ref_0}", "${Sub_1}"]',
        {
            "Sub_0": data_in[0],
            "Ref_0": data_in[1],
            "Sub_1": data_in[2],
        }]}
