

    var content = document.getElementsByClassName("content-wrapper");
function menuMobile(elem){
    document.querySelector('body').classList.toggle('open');
    elem.classList.toggle('fa');
    elem.classList.toggle('fa-bars');
    
    elem.classList.toggle('fas');
    elem.classList.toggle('fa-arrow-left');
    elem.style.marginTop='10px';
    document.querySelector('.menu-mobile-bg').height='100vh';
    
    
    document.querySelector('.menu-mobile').classList.toggle('z_index');
    
    
    }











    
    var element = document.getElementById("custom-search-box");
    function myFunction(clck) {
        
       
        
        clck.classList.toggle('fa');
        clck.classList.toggle('fa-search');
        clck.classList.toggle('fas');
        clck.classList.toggle('fa-arrow-up');
      
        if (element.style.display ==="none") { 
          element.style.display = 'block';
          element.classList.add('block-search');
          document.querySelector('.menu-mobile-bg').style.marginTop='105px';
          document.getElementById('menu').style.marginTop='105px';
        } 
        else {
          element.style.display = 'none';
          element.classList.remove('block-search');
          document.querySelector('.menu-mobile-bg').style.marginTop='60px';
          document.getElementById('menu').style.marginTop='60px';
        }
    
        
      }
    
    











    var menu=document.getElementById('menu');
    var nav=document.getElementById('nav-menu');
    var iconimg=nav.querySelectorAll('.icon');
    var header_menu=document.getElementById('header-menu');
    var form_menu=document.getElementById('form-menu');
    var spanmenu=nav.querySelectorAll('span');
    var linkmenu=nav.querySelectorAll('a');
    
    menu.style.zIndex='2000';
    
    var sticky=menu.offsetTop;
    function stickyfunc(){
      
      if(window.matchMedia('(min-width:1200px)').matches){
        
      if(window.pageYOffset>=sticky){
       
        menu.classList.add('sticky');
        header_menu.classList.add('sticky-header');
        menu.style.display='grid';
        menu.style.gridTemplateColumns='repeat(11,1fr)';
        header_menu.style.display='block';
        header_menu.style.gridColumn='span 2';
        form_menu.style.display='block';
        form_menu.style.gridColumn='span 2';
        nav.style.gridColumn='span 7';
        for(var i=0;i<iconimg.length;i++){

          iconimg[i].style.display='none';
          linkmenu[i].style.paddingTop='30px';
          spanmenu[i].style.fontSize='16px';
          spanmenu[i].style.gridColumn='span 1';

        }
      }else{
        menu.classList.remove('sticky');
        header_menu.classList.remove('sticky-header');
        header_menu.style.display='none';
        form_menu.style.display='none';
        menu.style.gridTemplateColumns='repeat(7,1fr)';
        for(var i=0;i<iconimg.length;i++){
          iconimg[i].style.display='inline-block';
          linkmenu[i].style.paddingTop='8px';
          spanmenu[i].style.fontSize='92%';
          spanmenu[i].style.gridColumn='span 1';
        }
      }
    }else if(window.matchMedia('(max-width:576px)').matches ){
    menu.style.display='none';
    
    menu.classList.remove('sticky');
    header_menu.classList.remove('sticky-header');
    header_menu.style.display='none';
    form_menu.style.display='none';
    menu.style.gridTemplateColumns='repeat(7,1fr)';
    for(var i=0;i<iconimg.length;i++){
      iconimg[i].style.display='inline-block';
      linkmenu[i].style.paddingTop='8px';
      spanmenu[i].style.fontSize='92%';
      spanmenu[i].style.gridColumn='span 1';
    }
    }
    }
    
    
    var question=document.getElementById('footer-part2').querySelectorAll('a');
    for(var i=5;i<question.length;i++){
      var width=window.innerWidth;
      if(width>991 && width<1200){
       
        question[i].style.display='none';
      }
    }