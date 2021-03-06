import logging

logger = logging.getLogger('exchangeService.Rates')
rates_file = ''
log_file = ''

def set_params(rfile, lfile):
    global rates_file
    global log_file

    rates_file = rfile
    log_file = lfile

def load_current_rates() -> dict:
    current_rates = {}

    with open(rates_file, "r") as f:
        for rate_line in f.readlines():
            temp_list = rate_line.strip().split("=")
            current_rates[temp_list[0]] = temp_list[1]

    logger.info('current rates loaded from file')
    return current_rates

def write_current_rates(current_rates: dict):
    with open(rates_file, "w") as f:
        for pairs in current_rates.keys():
            f.write(pairs + "=" + str(current_rates[pairs]) + "\n")
    logger.info('new rates written to file')

def calculate_currency_values(current_rates: dict, input_string: str) -> list:
    amount = float(input_string.split(" ")[0])
    currency = input_string.split(" ")[1]
    result = []

    for k in current_rates.keys():
        if currency == k[0:3:1]:
            result.append(str(amount * float(current_rates[k])) + " " + k[4:7:1])
        if currency == k[4:7:1]:
            result.append(str(round(amount / float(current_rates[k]), 2)) + " " + k[0:3:1])

    logger.info('currency values calculated')
    return result

def update_currency_rates(current_rates: dict, input_pair: str) -> dict:
    pair = input_pair.split("=")[0]
    rate = float(input_pair.split("=")[1])

    reversed_pair = pair[4:7:1] + "/" + pair[0:3:1]

    if reversed_pair in current_rates.keys():
        current_rates[reversed_pair] = round(1 / rate, 2)
    else:
        current_rates[pair] = rate

    write_current_rates(current_rates)

    logger.info('currency rates update completed')
    return current_rates