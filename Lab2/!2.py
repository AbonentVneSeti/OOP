class Color:
    ...

class Printer:
    def __init__(self, color : Color):
        self.Color = color


    @classmethod
    def print(cls,text : str, color : Color, position : tuple[int,int], symbol : str):
        ...



def get_font(font_path : str) -> dict[str : str, str : tuple[int,int]]:
    with open(file = font_path) as file:
        font = file.readlines()

    #mb check on errors

    size = tuple(int(i) for i in font[0][:-1].split(sep = 'x'))
    alphabet = dict()

    for char in range(1,len(font),size[0]+1):
        alphabet[font[char][:-1]] = [font[i][:-1] for i in range(char+1,char+size[0]+1)]

    alphabet['size'] = size

    return alphabet

def main():
    ...

if __name__ == "__main__":
    #main()
    a = get_font('font0.txt')
    print(a['A'])
