namespace programTests
{
       using System;
    class Program
    {
        static void Main(string[] args)
        {
            twoQuestionHello();
        }
        static void sayHello(String name)
        {
            Console.WriteLine($"Hello, {name}!");
        }
        static void twoQuestionHello()
        {
            bool isHappy;
            Console.WriteLine("What's your name?");
            String name = Console.ReadLine();
            Console.Write($"Hello, {name}! ");
            
            Console.WriteLine("How are you feeling today? (good/bad)");
            String response = Console.ReadLine();
            if (response.ToLower() == "good")
            {
                isHappy = true;
            }
            else
            {
                isHappy = false;
            }
            if (isHappy)
            {
                Console.WriteLine("Great! I'm glad you're happy today!");
            }
            else
            {
                Console.WriteLine("Too bad... I hope your day gets better.");
            }
        }
    }

}
