var accessModuleForm = document.getElementById("access_module");
var accesModuleBtn = document.getElementById('openAccess');
var complaintBtn = document.getElementById("openComp");
var complaintForm = document.getElementById("complaint");

let openMenu = false;

complaintBtn.addEventListener('click',() =>{
    if(!openMenu){
        complaintForm.style.height = 'fit-content';
        accessModuleForm.style.height = '0';
        complaintBtn.classList.add('active');

        openMenu = true;
    }


    else{
        complaintForm.style.height = '0';
        accessModuleForm.style.height = '500px';
        complaintBtn.classList.remove('active');
        accesModuleBtn.classList.add('active');

        openMenu = false;
    }
})
accesModuleBtn.addEventListener('click',() =>{
    if(!openMenu){
        accessModuleForm.style.height = '500px';
        accesModuleBtn.classList.add('active');
        complaintForm.style.height = '0';
        complaintBtn.classList.remove('active');

        openMenu = true;
    }


    else{
        accessModuleForm.style.height = '0';
        complaintForm.style.height = 'fit-content';
        accesModuleBtn.classList.remove('active');
        complaintBtn.classList.add('active');
        openMenu = false;
    }
})