from frontend import ExcelValidadorUI
from backend import process_excel, excel_to_sql
import logging
import sentry_sdk

sentry_sdk.init(
    dsn="https://d14279220e9a7752e90fc9cd3a0c6731@o4506810736902144.ingest.sentry.io/4506810779959296",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

# from logging import basicConfig

# basicConfig (
#     filename='logs.txt',
#     filemode='a',
#     encoding='utf-8',
#     format='%(levelname)s:%(asctime)s:%(message)s'
# )

def main():
    ui = ExcelValidadorUI()
    ui.display_header()

    upload_file = ui.upload_file()

    if upload_file:
        df, result, error = process_excel(upload_file)
        ui.display_results(result, error)

        if error:
            ui.display_wrong_message()
            logging.error("Planilha apresentava erros de Schema")
            sentry_sdk.capture_message("A planilha excel estava errada")
        elif ui.display_save_button():
            excel_to_sql(df)
            ui.display_success_message()
            logging.info("Foi enviado com sucesso ao banco SQL")
            sentry_sdk.capture_message("O banco SQL foi atualizado")

if __name__ == "__main__":
    main()