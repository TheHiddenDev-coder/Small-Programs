extends Node2D

var cash 			= 0.0
var cash_per_click 	= 1.0
var cash_per_second = 0.0

var cpc_upgr_cost 	= 1
var cpc_upgr_bonus 	= 1

var cps_upgr_cost 	= 1
var cps_upgr_bonus 	= 1

const COST_GROWTH_FACTOR = 1.3
const BONUS_GROWTH_FACTOR = 1.2


func _ready():
	update_ui()

func update_ui():
	$Score.text = "Cash: " + format_number(cash)
	$cash_per_second.text = "Cash/s: " + format_number(cash_per_second)
	$cash_per_click.text = "Cash/Click: " + format_number(cash_per_click)
	$cpc_upgr.text = "+ " + format_number(cpc_upgr_bonus) + "CASH/CLICK\nPRICE: " + format_number(cpc_upgr_cost)
	$cps_upgr.text = "+ " + format_number(cps_upgr_bonus) + "CASH/S\nPRICE: " + format_number(cps_upgr_cost)

func format_number(value):
	if value >= 1_000_000_000_000.0:
		return "%.1fT" % (value / 1_000_000_000_000.0)
	elif value >= 1_000_000_000.0:
		return "%.1fB" % (value / 1_000_000_000.0)
	elif value >= 1_000_000.0:
		return "%.1fM" % (value / 1_000_000.0)
	elif value >= 1_000.0:
		return "%.1fK" % (value / 1_000.0)
	else:
		return "%.1f" % value

func _on_main_pressed():
	cash += cash_per_click
	update_ui()

func _on_timer_timeout():
	cash += cash_per_second
	update_ui()
	$message_bar.text = ""

func _on_cpc_upgr_pressed():
	if cash >= cpc_upgr_cost:
		cash -= cpc_upgr_cost
		cash_per_click += cpc_upgr_bonus
		cpc_upgr_bonus *= BONUS_GROWTH_FACTOR
		cpc_upgr_cost *= COST_GROWTH_FACTOR
		update_ui()
	else:
		print("Can't afford")
		$message_bar.text = "You can't afford that upgrade"

func _on_cps_upgr_pressed():
	if cash >= cps_upgr_cost:
		cash -= cps_upgr_cost
		cash_per_second += cps_upgr_bonus
		cps_upgr_bonus *= BONUS_GROWTH_FACTOR
		cps_upgr_cost *= COST_GROWTH_FACTOR
		update_ui()
	else:
		print("Can't afford")
		$message_bar.text = "You can't afford that upgrade"
