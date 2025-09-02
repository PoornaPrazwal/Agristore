function store() {
    var usrName = document.getElementById('userName').value;
    var usrNum = document.getElementById('ph-number').value;
    var usrPw = document.getElementById('userpwd').value;
    let customer_users = JSON.parse(localStorage.getItem('users'));
    if(usrNum.length != 10){
        alert("Enter a valid phone number")
    }
    else{
        if(customer_users) {
            customer_users.push({name: usrName, password: usrPw});
            localStorage.setItem('users', JSON.stringify(customer_users));
            alert("Registration successful")
            location = location[href = "/html/customerlogin.html"];
        } 
        else {
            localStorage.setItem('users', JSON.stringify([{name: usrName, password: usrPw}]));
        }
    }
}



function check() {
    var usrName = document.getElementById('userName').value;
    var usrPw = document.getElementById('userpwd').value;
    let customer_users = JSON.parse(localStorage.getItem('users'))
    if(customer_users) {
        for (let u = 0; u < customer_users.length; u++){
            if (usrName == customer_users[u].name && usrPw == customer_users[u].password) {
                alert(`Welcome ${usrName} to Agri Business`);
                window.location.href = "/Agri business/html/index.html";
             }
        }
    } 
    else {
        localStorage.setItem('users', '[]');
    }
    return alert('Enter Valid username and password.');
}