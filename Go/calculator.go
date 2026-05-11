package main

import (
	"fmt"

	"github.com/fatih/color"
)

func main() {
	var op string
	var num1 float64
	var num2 float64
	var res float64

	fmt.Println("======== Calculator Program ========")
	fmt.Println("====================================")

	fmt.Print("Enter the operation to perform: ")
	_, err := fmt.Scanln(&op)
	if err != nil {
		color.Red("Invalid input:", err)
		return
	}

	fmt.Print("Enter the first number: ")
	_, err = fmt.Scanln(&num1)
	if err != nil {
		color.Red("Invalid input:", err)
		return
	}

	fmt.Print("Enter the second number: ")
	_, err = fmt.Scanln(&num2)
	if err != nil {
		color.Red("Invalid input:", err)
		return
	}

	switch op {
	case "+":
		res = num1 + num2
	case "-":
		res = num1 + num2
	case "*":
		res = num1 * num2
	case "/":
		if num2 == 0 {
			color.Red("Cannot divide by 0")
			return
		} else {
			res = num1 / num2
		}
	default:
		color.Red("Invalid operator\n")
		return
	}

	color.Green(fmt.Sprintf("%v %v %v = %v\n", num1, op, num2, res))
}
