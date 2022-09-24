import sys
from config import num_of_steps, template_of_report
from analytics import Research

if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            ex_class = Research(sys.argv[1])
            coin_list = ex_class.file_reader()
            ex_calculations = ex_class.Calculations(coin_list)
            coin_count = ex_calculations.counts()
            coin_fractions = ex_calculations.fractions(coin_count)
            ex_analytics = ex_class.Analytics(coin_list)
            coin_list_predict = ex_analytics.predict_random(num_of_steps)
            ex_calculations_predict = ex_class.Calculations(coin_list_predict)
            coin_count_predict = ex_calculations_predict.counts()
            ex_analytics.save_file(template_of_report.format(len(coin_list), coin_count[0], coin_count[1], coin_fractions[0], coin_fractions[1], num_of_steps, coin_count_predict[0], coin_count_predict[1]), 'report_of_data')
        except Exception:
            sys.exit("Error")
    else:
        sys.exit("Invalid argument!")
