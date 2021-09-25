const canvas = document.querySelector('canvas')
const ctx = canvas.getContext('2d')
setInterval(game, 1000/60);
window.addEventListener('keydown', keyPushed)
canvas.width = innerWidth
canvas.height = innerHeight
window.addEventListener('mousemove', mouseMove)

class Territory {
    constructor(name, owner, owner_color, x, y) {
        this.name = name
        this.owner = owner
        this.color = owner_color
        this.x = x
        this.y = y
    }

    draw() {
        this.drawing = new Path2D()
        this.drawing.arc(this.x, this.y, 20, 0, Math.PI*2, false)
        this.drawing.fillStyle = this.color
        this.drawing.fill()
    }
}

class Military {
    constructor(type, x, y) {
        this.type = type
        this.x = x
        this.y = y
    }
    draw() {
        this.drawing = new Path2D()
        this.drawing.arc(this.x, this.y, 15, 0, Math.PI*2, false)
        this.drawing.fillStyle = this.color
        this.drawing.fill()
    }
}

const centerX = canvas.width/2
const centerY = canvas.height/2
let londinium = new Territory("Londinium", "England", "blue", 100, 100)
let normandy = new Territory("Normandy", "France", "green", 300, 100)

function game() {
    function changeColor(object, color) {
        object.color = color
    }
    londinium.draw()
    normandy.draw()
}

function mouseMove(event) {
    if (event.isPointInPath(londinium, event.offsetX, event.offsetY)) {
      londinium.color = 'green';
      console.log("Hovered over dot!")
    }  
}

function keyPushed(evt) {
    switch(evt.keyCode) {
        case 37:
            console.log("You pressed left arrow!")
            color = "green"
            break;
        case 38:
            console.log("You pressed up arrow!")
            color = "blue"
            break;
        case 39:
            console.log("You pressed right arrow!")
            color = "red"
            break;
        case 40:
            console.log("You pressed down arrow!")
            color = "yellow"
            break;
    }
}