/*
const x = document.querySelectorAll("a.next-issue")
var count = 0
var index = 0
x.forEach(z => {
    count = count + 1
})
*/

/*
function move_carrusel(){
    if (index + 1 == count){
        x[index].click()
        index = 0
    }else{
        x[index].click()
        index = index + 1

    }

}
*/

var sha256 = function sha256(ascii) {
    function rightRotate(value, amount) {
        return (value >>> amount) | (value << (32 - amount));
    };

    var mathPow = Math.pow;
    var maxWord = mathPow(2, 32);
    var lengthProperty = 'length'
    var i, j; // Used as a counter across the whole file
    var result = ''

    var words = [];
    var asciiBitLength = ascii[lengthProperty] * 8;

    //* caching results is optional - remove/add slash from front of this line to toggle
    // Initial hash value: first 32 bits of the fractional parts of the square roots of the first 8 primes
    // (we actually calculate the first 64, but extra values are just ignored)
    var hash = sha256.h = sha256.h || [];
    // Round constants: first 32 bits of the fractional parts of the cube roots of the first 64 primes
    var k = sha256.k = sha256.k || [];
    var primeCounter = k[lengthProperty];
    /*/
    var hash = [], k = [];
    var primeCounter = 0;
    //*/

    var isComposite = {};
    for (var candidate = 2; primeCounter < 64; candidate++) {
        if (!isComposite[candidate]) {
            for (i = 0; i < 313; i += candidate) {
                isComposite[i] = candidate;
            }
            hash[primeCounter] = (mathPow(candidate, .5) * maxWord) | 0;
            k[primeCounter++] = (mathPow(candidate, 1 / 3) * maxWord) | 0;
        }
    }

    ascii += '\x80' // Append Ƈ' bit (plus zero padding)
    while (ascii[lengthProperty] % 64 - 56) ascii += '\x00' // More zero padding
    for (i = 0; i < ascii[lengthProperty]; i++) {
        j = ascii.charCodeAt(i);
        if (j >> 8) return; // ASCII check: only accept characters in range 0-255
        words[i >> 2] |= j << ((3 - i) % 4) * 8;
    }
    words[words[lengthProperty]] = ((asciiBitLength / maxWord) | 0);
    words[words[lengthProperty]] = (asciiBitLength)

    // process each chunk
    for (j = 0; j < words[lengthProperty];) {
        var w = words.slice(j, j += 16); // The message is expanded into 64 words as part of the iteration
        var oldHash = hash;
        // This is now the undefinedworking hash", often labelled as variables a...g
        // (we have to truncate as well, otherwise extra entries at the end accumulate
        hash = hash.slice(0, 8);

        for (i = 0; i < 64; i++) {
            var i2 = i + j;
            // Expand the message into 64 words
            // Used below if 
            var w15 = w[i - 15],
                w2 = w[i - 2];

            // Iterate
            var a = hash[0],
                e = hash[4];
            var temp1 = hash[7] +
                (rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25)) // S1
                +
                ((e & hash[5]) ^ ((~e) & hash[6])) // ch
                +
                k[i]
                // Expand the message schedule if needed
                +
                (w[i] = (i < 16) ? w[i] : (
                    w[i - 16] +
                    (rightRotate(w15, 7) ^ rightRotate(w15, 18) ^ (w15 >>> 3)) // s0
                    +
                    w[i - 7] +
                    (rightRotate(w2, 17) ^ rightRotate(w2, 19) ^ (w2 >>> 10)) // s1
                ) | 0);
            // This is only used once, so *could* be moved below, but it only saves 4 bytes and makes things unreadble
            var temp2 = (rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22)) // S0
                +
                ((a & hash[1]) ^ (a & hash[2]) ^ (hash[1] & hash[2])); // maj

            hash = [(temp1 + temp2) | 0].concat(hash); // We don't bother trimming off the extra ones, they're harmless as long as we're truncating when we do the slice()
            hash[4] = (hash[4] + temp1) | 0;
        }

        for (i = 0; i < 8; i++) {
            hash[i] = (hash[i] + oldHash[i]) | 0;
        }
    }

    for (i = 0; i < 8; i++) {
        for (j = 3; j + 1; j--) {
            var b = (hash[i] >> (j * 8)) & 255;
            result += ((b < 16) ? 0 : '') + b.toString(16);
        }
    }
    return result;
};



let asd = []
asd.push("admin@admin.com", "f093416ed7e67ffba824a1c3f942e7748931e39cf81d8eae4632167d4ceb0f25")
asd.push("dnorde290@gmail.com", "ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f")

console.log("Hello there", asd)


/*Session Management */

function save_users() {
    localStorage.setItem("users", asd)
}

function setregisterflag() {
    sessionStorage.setItem("register", true)
}

var ls = ""

if (localStorage.length == 0) {
    save_users()
    ls = localStorage.getItem("users")
} else {
    ls = localStorage.getItem("users")
}


if (ls.length != asd.length) {
    if (!sessionStorage.getItem("register")) {
        save_users()
        ls = localStorage.getItem("users")
    }
}

var login_users = ls.split(",")

function check_email_exist(value) {
    let user_position = 0
    for (let z = 0; z < asd.length; z++) {
        if (value == asd[z]) {
            return true
        }
    }
    return false
}

function is_email(email) {
    /*
    Los Caracteres admitidos son a-z, 0-9, @, -, _, y .
    A-Z   65-90
    a-z   97-122
    0-9   48-57
    @     64
    -     45
    _     95
    .     46
    */
    let email_array = email.split("")
    email_array.forEach(char => {
        /* Por cada caracter en email*/
        let ascii = char.charCodeAt(0) // esta linea convierte el caracter en codigo ascii
        if (!((ascii >= 65 && ascii <= 90) || (ascii >= 97 && ascii <= 122) || (ascii >= 48 && ascii <= 57) || ([64, 45, 95, 46].indexOf(char) == -1))) {
            console.log("bad email detected", ascii, char, email)
            return false
        }
        let array = email.split("@")
        if (array[1].includes(".")) {
            return true
        } else {
            console.log("email does not provide a correct domain")
            return false
        }
    })
}

function validate_passwd(email, token) {
    let count = 0
    for (let i = 0; i < asd.length; i++) {
        if (i % 2 == 0 && asd[i] == email && asd[i + 1] == token) {
            return true
        }
    }
    return false
}


/* Slideshow function */
function apply_patch(value) {
    for (let i = 0; i < count; i++) {
        if (i == value) {
            x[i].style.display = "block"
            console.log("Le Block ", value)
        } else {
            x[i].style.display = "none"
            console.log("None", value)
        }
    }
    console.log("------------------------")

}

function move_carrusel() {
    if (index + 1 == count) {
        index = 0
        apply_patch(index)
    } else {
        index++
        apply_patch(index)
    }
}

function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

                break;
            }
        }
    }

    return cookieValue;
}


/* Sign UP Validation*/
function check_form_signup(e) {
    let lock = 0
    e.preventDefault();
    var user_name = $('#user_name').val();
    var email = $('#email').val();
    var password = $('#passw1').val();
    var password2 = $('#passw2').val();
    $(".error").remove();
    if (user_name.length < 5) {
        $('#user_name').after('<span class="error" style="color: red;">User must have more than 5 characters.</span>');
    }
    if (email.length < 1) {
        $('#email').after('<span class="error" style="color: red;">This field is required.</span>');
    } else {
        // NO FUNCIONA POR ALGUNA EXTRANHA RAZON
        var regEx = /^[A-Z0-9][A-Z0-9._%+-]{0,63}@(?:[A-Z0-9-]{1,63}\.){1,125}[A-Z]{2,63}$/;
        var validEmail = regEx.test(email);
        if (!validEmail) {
            $('#email').after('<span class="error" style="color: red">Enter a valid email.</span>');
        }
        if (is_email(email)) {
            $('#email').after('<span class="error" style="color: red">Enter a valid email.</span>');
        } else {
            lock++
        }
    }
    if (password.length < 8) {
        console.log("1passwd", password)
        $('#passw1').after('<span class="error" style="color: red;">Password must be at least 8 characters long.</span>');
    }
    if (password != password2) {
        $('#passw2').after('<span class="error" style="color: red;">Password must be equal.</span>');
    }
}

/*
$(document).ready(
    function() {
        $('#first_form').onsubmit(function(e) {
            let lock = 0
            e.preventDefault();
            var user_name = $('#user_name').val();
            var email = $('#email').val();
            var password = $('#passw1').val();
            var password2 = $('#passw2').val();
            $(".error").remove();
            if (user_name.length < 5) {
                $('#user_name').after('<span class="error" style="color: red;">User must have more than 5 characters.</span>');
            }
            if (email.length < 1) {
                $('#email').after('<span class="error" style="color: red;">This field is required.</span>');
            } else {
                // NO FUNCIONA POR ALGUNA EXTRANHA RAZON
                var regEx = /^[A-Z0-9][A-Z0-9._%+-]{0,63}@(?:[A-Z0-9-]{1,63}\.){1,125}[A-Z]{2,63}$/;  
                var validEmail = regEx.test(email);  
                if (!validEmail) {  
                    $('#email').after('<span class="error" style="color: red">Enter a valid email.</span>');  
                }
                if (is_email(email)) {
                    $('#email').after('<span class="error" style="color: red">Enter a valid email.</span>');
                } else {
                    lock++
                }
            }
            if (password.length < 8) {
                console.log("1passwd", password)
                $('#passw1').after('<span class="error" style="color: red;">Password must be at least 8 characters long.</span>');
            }
            if (password != password2) {
                $('#passw2').after('<span class="error" style="color: red;">Password must be equal.</span>');
            }
            if (lock == 1) {
                return true
                /*
                fetch("/signup/", {
                    method: 'POST',
                    body: JSON.stringify({
                        "user": user_name,
                        "email": email,
                        "passwd": sha256(password)
                    })
                })*/
/*
if (check_email_exist(email)) { //comprueba si el email existe
    $('#email').after('<span class="error" style="color: red">Provided email already exist.</span>');
} else {
    // Register new user 
//TODO: manejar nombres de usuario?
 
let token = sha256(password)
asd.push(email, token)
save_users()
setregisterflag()
window.location = '/Template/User/user.html' //Redirect to users page
}
 
}
})
}
);
*/
/* Sign IN Validation*/



/*
     $('form[id="second_form"]').validate({  
       rules: {  
        user_name: 'required',  
         email: {  
           required: true,  
           email: true,  
         },  
         passw1: {  
           required: true,  
           minlength: 8,  
         } 
         passw2: {  
            required: true,  
            minlength: 8,  
          }  
  
       },  
       messages: {  
        user_name: 'This field is required',   
         email: 'Enter a valid email',  
         passw1: {  
           minlength: 'Password must be at least 8 characters long'  
         }  
       },  
       submitHandler: function(form) {  
         form.submit();  
       }  
     });  
   });  
*/
/*
$("#formValidation").validate({
    rules:{
        username:{
            minlength: 5
        },
        email:{
            email:true
            
        }
    },
    messages: {
        username:{
            required: "Please enter your username",
            minlength: "Username at least 5 characters"
        },
        email: "Please enter your email",
    },
    submitHandler:function(form){
        form.submit();
    }
 
});
*/


/* Determina si la pagina contiene el carrusel o no si no lo tiene, no ejecuta el codigo */
const x = document.querySelectorAll("div.itemCarrusel")
console.log(x)
if (x.length == 0) {
    console.log("There is not slideshow around here :(")
} else {
    x[0].style.display = "block"

    var count = x.length
    var index = 0

    setInterval(move_carrusel, 5000)
}

function product(id) {
    window.location.href = "/Template/product/" + id
}

function garage(id) {
    window.location.href = "/Template/garage/" + id
}

//search
document.addEventListener('keyup', e => {
    if (e.target.matches('#buscador')) {
        document.querySelectorAll('div.info-product').forEach(product => {
            product.textContent.toLowerCase().include(e.target.value);
            product.classList.remove('filtro')
            product.classList.add('filtro');
        })
    }
})
