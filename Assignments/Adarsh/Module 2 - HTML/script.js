setInterval(showTime, 1000);
function showTime() {
    let time = new Date();
    let hour = time.getHours();
    let min = time.getMinutes();
    let sec = time.getSeconds();
    am_pm = "AM";

    if (hour > 12) {
        hour -= 12;
        am_pm = "PM";
    }
    if (hour == 0) {
        hr = 12;
        am_pm = "AM";
    }

    hour = hour < 10 ? "0" + hour : hour;
    min = min < 10 ? "0" + min : min;
    sec = sec < 10 ? "0" + sec : sec;

    let currentTime = "Time : " + hour + ":" 
            + min + ":" + sec + am_pm;

    document.getElementById("clock")
            .innerHTML = currentTime;
}

var programmingLanguages = [];

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop1(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
    programmingLanguages.push(data)
}

function drop2(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
    programmingLanguages = programmingLanguages.filter(e => e !== data)
}

function submitAction() {
    console.log("hello");
    let myForm = document.getElementById('regForm');
    let formData = new FormData(myForm);
    let name = formData.get('name');
    let formValues = {
        name:formData.get('name'),
        collegeName:formData.get('collegeName'),
        collegeAddr:formData.get('collegeAddr'),
        pincode:formData.get('pincode'),
        age:formData.get('age'),
        dob:formData.get('dob'),
        gender:formData.get('gender'),
        dept:formData.get('department'),
        phone:formData.get('phone'),
        email:formData.get('email'),
        hobbies:formData.getAll('hobbies'),
    };
    console.log(formValues)
    let main = document.getElementById("main");
    main.innerHTML = "<h1>Submitted data</h1>"
    main.innerHTML += "<table><tr><th>Field</th><th>Value</th></tr><tr><td>Name</td><td>"+formValues.name+"\
                        </td></tr><tr><td>College Name</td><td>"+formValues.collegeName+"\
                        </td></tr><tr><td>College Address</td><td>"+formValues.collegeAddr+"\
                        </td></tr><tr><td>pincode</td><td>"+formValues.pincode+"\
                        </td></tr><tr><td>Age</td><td>"+formValues.age+"\
                        </td></tr><tr><td>Date of Birth</td><td>"+formValues.dob+"\
                        </td></tr><tr><td>Gender</td><td>"+formValues.gender+"\
                        </td></tr><tr><td>Department</td><td>"+formValues.dept+"\
                        </td></tr><tr><td>Phone</td><td>"+formValues.phone+"\
                        </td></tr><tr><td>Email</td><td>"+formValues.email+"\
                        </td></tr><tr><td>Hobbies</td><td>"+formValues.hobbies+"\
                        </td></tr><tr><td>Programming skills</td><td>"+programmingLanguages+"</table>"
}

showTime();