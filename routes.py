from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from dao.stockdao import StockDAO
from analise import AnalysisService

main_bp = Blueprint('main', __name__, url_prefix='/main')
stock_dao = StockDAO()


@main_bp.route("/")
@main_bp.route("/dashboard")
@login_required
def dashboard():
    stocks = stock_dao.get_user_stocks(current_user.id)
    return render_template('dashboard.html', stocks=stocks)


@main_bp.route("/stock/add", methods=['POST'])
@login_required
def add_stock():
    ticker = request.form.get('ticker')
    quantity = int(request.form.get('quantity'))

    stock_dao.add_stock(ticker, quantity, current_user.id)
    flash(f'Ação {ticker} adicionada com sucesso!', 'success')
    return redirect(url_for('main.dashboard'))


@main_bp.route("/stock/delete/<int:stock_id>")
@login_required
def delete_stock(stock_id):
    if stock_dao.delete_stock(stock_id, current_user.id):
        flash('Ação removida da carteira.', 'info')
    else:
        flash('Erro ao remover ação', 'danger')
    return redirect(url_for('main.dashboard'))


@main_bp.route("/stock/edit/<int:stock_id>", methods=['POST'])
@login_required
def edit_stock(stock_id):
    quantity = int(request.form.get('quantity'))
    if stock_dao.update_stock(stock_id, current_user.id, quantity):
        flash('Ação atualizada com sucesso!', 'success')
    else:
        flash('Erro ao atualizar ação', 'danger')

    return redirect(url_for('main.dashboard'))


@main_bp.route("/analysis/<ticker>")
@login_required
def analysis(ticker):
    data = AnalysisService.get_fundamentals(ticker)

    if not data:
        flash(f'Não foi possível obter dados para {ticker}', 'warning')
        return redirect(url_for('main.dashboard'))


    graham_price = AnalysisService.calculate_graham_value(data['lpa'], data['vpa'])

    dcf_price = AnalysisService.get_dcf_valuation(ticker)

    upside = 0
    if graham_price > 0 and data['price'] > 0:
        upside = ((graham_price - data['price']) / data['price']) * 100

    return render_template('analise.html',
                           ticker=ticker,
                           data=data,
                           graham_price=graham_price,
                           dcf_price=dcf_price,
                           upside=upside)

