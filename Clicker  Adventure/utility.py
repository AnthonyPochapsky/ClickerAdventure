def input_loop(Intructional_text):
    while True:
        #If the player corrects their mistake by correctly inputting a number that is also between 1 and 50, then break the loop and return the value.
        try:
            try_again=int(input(Intructional_text))
            if 1<=try_again<=50:
                break
            else:
                print("Only values between 1 and 50 allowed")
        except ValueError:
            print("Please only include numbers")
    return try_again