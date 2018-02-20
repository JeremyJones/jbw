from .calculate_natural_log import calculate_natural_log


class set_natural_log_behaviour:

    def set_natural_log(self, feed):
        columns = feed.data['dataset']['column_names']
        previous_price = None

        for rownum, data in enumerate(feed.data['dataset']['data']):
            info = dict(zip(columns, data))

            if previous_price is not None:
                info['Natural Log'] = calculate_natural_log(
                                      float(info['Close']) - previous_price)
            else:
                info['Natural Log'] = 0.0

            previous_price = float(info['Close'])
            data.append(info['Natural Log'])

        feed.data['dataset']['column_names'].append('Natural Log')
