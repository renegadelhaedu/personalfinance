import yfinance as yf
import math


class AnalysisService:
    @staticmethod
    def get_fundamentals(ticker):
        """Busca dados fundamentais via yfinance"""
        # Adiciona .SA se for ação brasileira e não tiver a extensão
        if not ticker.endswith('.SA') and not ticker.endswith('.US'):
            ticker = f"{ticker}.SA"

        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            # Tratamento de erro caso a ação não tenha dados (ex: FIIs ou dados faltantes)
            if 'regularMarketPrice' not in info:
                return None

            data = {
                'price': info.get('currentPrice', 0),
                'name': info.get('longName', ticker),
                'sector': info.get('sector', 'N/A'),
                # Indicadores de Valuation Relativo
                'pe_ratio': info.get('trailingPE', 0),  # P/L
                'pb_ratio': info.get('priceToBook', 0),  # P/VP
                'dividend_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                # Indicadores de Qualidade
                'roe': info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0,
                'profit_margins': info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0,
                # Dados para Fórmula de Graham
                'vpa': info.get('bookValue', 0),  # Valor Patrimonial por Ação
                'lpa': info.get('trailingEps', 0)  # Lucro por Ação
            }

            return data
        except Exception as e:
            print(f"Erro ao buscar dados: {e}")
            return None

    @staticmethod
    def calculate_graham_value(lpa, vpa):
        """
        Fórmula de Benjamin Graham: Raiz Quadrada de (22.5 * LPA * VPA)
        Onde 22.5 é o produto de P/L máximo (15) e P/VP máximo (1.5)
        """
        if lpa > 0 and vpa > 0:
            try:
                fair_value = math.sqrt(22.5 * lpa * vpa)
                return fair_value
            except ValueError:
                return 0
        return 0

    @staticmethod
    def get_dcf_valuation(ticker, growth_rate=0.08, discount_rate=0.12, terminal_growth=0.03):
        """
        Calcula o DCF Simplificado (2 Estágios).
        growth_rate: Crescimento estimado para os próximos 5 anos (8%)
        discount_rate: Taxa de desconto/WACC (12% conservador)
        terminal_growth: Crescimento perpétuo (inflação ~2.5%)
        """
        if not ticker.endswith('.SA') and not ticker.endswith('.US'):
            ticker = f"{ticker}.SA"

        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            # 1. Tentar obter o Free Cash Flow (FCF)
            # O yfinance às vezes tem o campo pronto, às vezes precisamos calcular
            fcf = info.get('freeCashflow')

            if fcf is None:
                # Tentativa manual: Cash Operacional - CapEx
                cashflow_stmt = stock.cashflow
                if cashflow_stmt is not None and not cashflow_stmt.empty:
                    try:
                        # Pega o dado mais recente (primeira coluna)
                        operating_cash_flow = cashflow_stmt.loc['Total Cash From Operating Activities'].iloc[0]
                        capex = cashflow_stmt.loc['Capital Expenditures'].iloc[0]
                        fcf = operating_cash_flow + capex  # Capex geralmente é negativo, então somamos
                    except:
                        return 0  # Não foi possível calcular
                else:
                    return 0

            # Se FCF for negativo ou zero, o modelo DCF quebra
            if fcf <= 0:
                return 0

            # 2. Dados de Balanço
            cash_equivalents = info.get('totalCash', 0)
            total_debt = info.get('totalDebt', 0)
            shares_outstanding = info.get('sharesOutstanding', 0)

            if shares_outstanding == 0:
                return 0

            # --- CÁLCULO DO MODELO ---

            future_cash_flows = []

            # Estágio 1: Projeção para 5 anos
            for i in range(1, 6):
                # Projeta o crescimento
                projected_fcf = fcf * ((1 + growth_rate) ** i)
                # Traz a valor presente
                discounted_fcf = projected_fcf / ((1 + discount_rate) ** i)
                future_cash_flows.append(discounted_fcf)

            sum_pv_cash_flows = sum(future_cash_flows)

            # Estágio 2: Valor Terminal (Perpetuidade)
            # Fórmula: (FCF do ano 5 * (1 + g_perpétuo)) / (WACC - g_perpétuo)
            fcf_year_5 = fcf * ((1 + growth_rate) ** 5)
            terminal_value = (fcf_year_5 * (1 + terminal_growth)) / (discount_rate - terminal_growth)

            # Traz o Valor Terminal a Valor Presente
            pv_terminal_value = terminal_value / ((1 + discount_rate) ** 5)

            # Valor da Empresa (Enterprise Value)
            enterprise_value = sum_pv_cash_flows + pv_terminal_value

            # Valor do Acionista (Equity Value) = EV + Caixa - Dívida
            equity_value = enterprise_value + cash_equivalents - total_debt

            # Preço Justo por Ação
            fair_price = equity_value / shares_outstanding

            return fair_price

        except Exception as e:
            print(f"Erro no DCF para {ticker}: {e}")
            return 0