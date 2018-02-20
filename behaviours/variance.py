from .calculate_variance_reqs import calculate_variance_reqs as calculate_variance
# from .calculate_variance_npvar import calculate_variance_npvar as calculate_variance


class set_variance_behaviour:

    def set_variance(self, feed):
        columns = feed.data['dataset']['column_names']
        all_prices = []

        for _, data in enumerate(feed.data['dataset']['data']):
            info = dict(zip(columns, data))
            all_prices.append(float(info['Close']))

        for _, data in enumerate(feed.data['dataset']['data']):
            info = dict(zip(columns, data))
            info['Variance'] = calculate_variance(
                               float(info['Close']), all_prices)
            data.append(info['Variance'])

        feed.data['dataset']['column_names'].append('Variance')
