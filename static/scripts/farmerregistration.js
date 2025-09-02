function store() {
    var usrName = document.getElementById('userName').value;
    var usrNum = document.getElementById('ph-number').value;
    var usrPw = document.getElementById('pwd').value;
    let farmer_users = JSON.parse(localStorage.getItem('users'));
    if(usrNum.length != 10){
        alert("Enter a vaalid phone number")
    }
    else{
        if(farmer_users) {
            farmer_users.push({name: usrName, password: usrPw});
            localStorage.setItem('users', JSON.stringify(farmer_users));
            alert("Registration successful")
            return location.replace("./farmerlogin.html");
        } 
        else {
            localStorage.setItem('users', JSON.stringify([{name: usrName, password: usrPw}]));
        }
    }
}



function check() {
    var usrName = document.getElementById('userName').value;
    var usrPw = document.getElementById('userpwd').value;
    let farmer_users = JSON.parse(localStorage.getItem('users'))
    if(farmer_users) {
        for (let u = 0; u < farmer_users.length; u++){
            if (usrName == farmer_users[u].name && usrPw == farmer_users[u].password) {
                alert(`Welcome ${usrName} to Agri Business`);
                return location.replace("/html/index.html");
             }
        }
    } 
    else {
        localStorage.setItem('users', '[]');
    }
    return alert('Access denied. Valid username and password is required.');
}