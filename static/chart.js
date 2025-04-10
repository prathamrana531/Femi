let circle = document.querySelectorAll(".circle");
let part1 = document.querySelector(".part1");
let part2 = document.querySelector(".part2");

let arrPart1 = ["Step:", "Step:", "Step:", "Step:"];
let arrPart2 = [`Our first layer is sequential as there's only a single input. Since it is a picture we need to flatten the RGB content.`,
    `We have then used batch normalisation layer to normalise the mean output and standard deviation.`,
    `Then we have densely connected 4 layers. Again, to normalise the output we have used batch normalisation and we have used the activation function 'softmax'.`,
    `We have compiled the whole model using optimiser 'Adam' , handled losses using 'categoricalCrossentropy' and using metrics 'accuracy'. We have set up 50 epochs for better accuracy.`];

for (let i = 0; i < 4; i++) {
    circle[i].addEventListener("click", function () {
        change(i);
    });
}

function change(i) {
    part1.innerHTML = arrPart1[i];
    part2.innerHTML = arrPart2[i];
    for (let j = 0; j < 4; j++) {
        if (i != j) {
            circle[j].style.borderWidth = "3px";
        }
    }
    circle[i].style.borderWidth = "thick";
}

