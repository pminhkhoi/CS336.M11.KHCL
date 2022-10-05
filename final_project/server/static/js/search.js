let jcrop


function readURL(input) {
    let el = document.getElementById("searchbutton")

    let imageDiv = document.getElementById("resultImage")

    while (imageDiv.firstChild) imageDiv.removeChild(imageDiv.firstChild)

    if (el) {
        el.remove()
    }

    if (jcrop) {
        jcrop.destroy()
    }

    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            $('#queryImage').attr('src', e.target.result);
            jcrop = Jcrop.attach('queryImage')


            let btn = document.createElement("button")
            btn.innerHTML = "Search"
            btn.id = "searchbutton"
            btn.addEventListener("click", async () => {
                btn.style.display = 'none'

                let loadingIcon = document.createElement('div')
                loadingIcon.className = "loader"

                document.getElementById("searchdiv").append(loadingIcon)

                let data = new FormData()
                data.append('file', input.files[0])

                let responseData

                await fetch("/test", {
                    method: 'POST',
                    headers: {
                        'pos': `${(jcrop.active == null) ? 'none' : JSON.stringify(jcrop.active.pos)}`
                    },
                    body: data
                }).then(response => response.json()).then((respData) =>
                    responseData = respData,
                )

                let resultText = document.createElement("h2")
                text = document.createTextNode(`Result: `)
                resultText.appendChild(text)

                let resultBox = document.getElementById("resultImage")

                resultBox.appendChild(resultText)

                for (i = 0; i < responseData.length; i++) {
                    let newImageBox = document.createElement("div")
                    let img = document.createElement("img")

                    img.src = responseData[i][0]
                    img.width = 250
                    img.height = 250
                    p = document.createElement("p")
                    text = document.createTextNode(`Similarity: ${1 - responseData[i][1]}`)

                    p.appendChild(text)
                    newImageBox.append(img)
                    newImageBox.append(p)

                    resultBox.append(newImageBox)

                    loadingIcon.style.display = 'none'
                }
                resultBox.style.display = 'block'
            })
            document.getElementById("searchdiv").appendChild(btn)
        }
        reader.readAsDataURL(input.files[0]);
    }
}

window.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.getElementById("imageInput")

    imageInput.addEventListener("change", (e) => {
        readURL(e.target)
    })
})

