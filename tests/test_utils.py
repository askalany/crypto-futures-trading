from enums import (
    TIF,
    OrderType,
    PositionSide,
    PriceMatchNone,
    PriceMatchQueue,
    Side,
    TickerSymbol,
)
from utils import create_order, get_scaled_amounts, split_into_num


def order_value():
    symbol = TickerSymbol.BTCUSDT
    side = Side.BUY
    quantity = 1.0
    price = 1.0
    position_side = PositionSide.LONG
    order_type = OrderType.LIMIT
    time_in_force = TIF.GTC
    price_match = PriceMatchNone.NONE
    return (
        symbol,
        side,
        quantity,
        price,
        position_side,
        order_type,
        time_in_force,
        price_match,
    )


def test_create_order_price():
    (
        symbol,
        side,
        quantity,
        price,
        position_side,
        order_type,
        time_in_force,
        price_match,
    ) = order_value()
    order = create_order(
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=price,
        position_side=position_side,
        order_type=order_type,
        time_in_force=time_in_force,
        price_match=price_match,
    )
    assert "price" in order


def test_create_order_price_value():
    (
        symbol,
        side,
        quantity,
        price,
        position_side,
        order_type,
        time_in_force,
        price_match,
    ) = order_value()
    order = create_order(
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=price,
        position_side=position_side,
        order_type=order_type,
        time_in_force=time_in_force,
        price_match=price_match,
    )
    assert order["price"] == price


def test_create_order_price_match():
    (
        symbol,
        side,
        quantity,
        price,
        position_side,
        order_type,
        time_in_force,
        price_match,
    ) = order_value()
    order = create_order(
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=price,
        position_side=position_side,
        order_type=order_type,
        time_in_force=time_in_force,
        price_match=PriceMatchQueue.QUEUE,
    )
    assert "priceMatch" in order


def test_scaled_amounts():
    expected_list = [
        5.865743125390515,
        5.924400556644421,
        5.9836445622108645,
        6.043481007832973,
        6.103915817911304,
        6.164954976090415,
        6.226604525851319,
        6.2888705711098325,
        6.351759276820931,
        6.415276869589142,
        6.4794296382850325,
        6.544223934667883,
        6.609666174014562,
        6.675762835754708,
        6.742520464112254,
        6.809945668753378,
        6.87804512544091,
        6.94682557669532,
        7.0162938324622734,
        7.086456770786897,
        7.157321338494765,
        7.228894551879714,
        7.301183497398512,
        7.374195332372497,
        7.447937285696223,
        7.522416658553184,
        7.597640825138715,
        7.673617233390103,
        7.750353405724004,
        7.827856939781245,
        7.906135509179058,
        7.985196864270848,
        8.065048832913558,
        8.145699321242693,
        8.22715631445512,
        8.30942787759967,
        8.392522156375668,
        8.476447377939424,
        8.56121185171882,
        8.646823970236008,
        8.733292209938368,
        8.820625132037751,
        8.908831383358129,
        8.99791969719171,
        9.087898894163628,
        9.178777883105266,
        9.270565661936319,
        9.36327131855568,
        9.456904031741239,
        9.551473072058652,
        9.646987802779238,
        9.74345768080703,
        9.840892257615101,
        9.939301180191253,
        10.038694191993166,
        10.139081133913097,
        10.240471945252226,
        10.342876664704749,
        10.446305431351796,
        10.550768485665316,
        10.656276170521968,
        10.76283893222719,
        10.87046732154946,
        10.979171994764956,
        11.088963714712605,
        11.199853351859732,
        11.31185188537833,
        11.424970404232113,
        11.539220108274433,
        11.654612309357177,
        11.771158432450749,
        11.888870016775257,
        12.007758716943009,
        12.12783630411244,
        12.249114667153563,
        12.3716058138251,
        12.49532187196335,
        12.620275090682984,
        12.746477841589813,
        12.873942620005712,
        13.002682046205768,
        13.132708866667828,
        13.264035955334505,
        13.39667631488785,
        13.53064307803673,
        13.665949508817096,
        13.80260900390527,
        13.940635093944321,
        14.080041444883765,
        14.220841859332603,
        14.363050277925927,
        14.506680780705189,
        14.651747588512238,
        14.798265064397363,
        14.946247715041334,
        15.09571019219175,
        15.246667294113665,
        15.399133967054802,
        15.55312530672535,
        15.708656559792034,
    ]
    expected_sum = 1000
    result = get_scaled_amounts(total_amount=1000, volume_scale=1.01, num=100)
    assert result == expected_list


def test_scaled_amounts_sum():
    expected_sum = 1000
    result = get_scaled_amounts(total_amount=1000, volume_scale=1.01, num=100)
    assert sum(result) == expected_sum


def test_split_into_num():
    num = 5
    length = 199
    multiples, remainder = split_into_num(num=num, length=length)
    assert (multiples, remainder) == (39, 4)
