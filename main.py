import argparse
import neuronet

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--image")

    args = parser.parse_args()

    result = neuronet.resolve(args.image)

    for gender in result[0]: print(gender)
    for age in result[1]: print(age + " years old")

if __name__ == "__main__": main()