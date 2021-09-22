const canvas = document.querySelector('canvas')
const ctx = canvas.getContext('2d')

canvas.width = innerWidth
canvas.height = innerHeight

class Territory {
    constructor(name, owner, owner_color, x, y) {
        this.name = name
        this.owner = owner
        this.color = owner_color
        //this.image = image
        this.x = x
        this.y = y
    }

    draw() {
        ctx.beginPath()
        ctx.arc(this.x, this.y, 20, 0, Math.PI*2, false)
        ctx.fillStyle = this.color
        ctx.fill()
    }
}

class Military {
    constructor(type, x, y) {
        this.type = type
        this.x = x
        this.y = y
    }
    draw() {
        ctx.beginPath()
        ctx.arc(this.x, this.y, 15, 0, Math.PI*2, false)
        ctx.fillStyle = this.color
        ctx.fill()
    }
}


const centerX = canvas.width/2
const centerY = canvas.height/2

let londinium = new Territory("Londinium", "England", "blue", 100, 100)
let normandy = new Territory("Normandy", "France", "green", 300, 100)

londinium.draw()
normandy.draw()

window.addEventListener('keydown', keyPushed)
function keyPushed(evt) {
    switch(evt.keyCode) {
        case 37:
            console.log("You pressed left arrow!")
            londinium.color = "green"
            break;
        case 38:
            console.log("You pressed up arrow!")
            londinium.color = "blue"
            break;
        case 39:
            console.log("You pressed right arrow!")
            londinium.color = "red"
            break;
        case 40:
            console.log("You pressed down arrow!")
            londinium.color = "yellow"
            break;
    }
}