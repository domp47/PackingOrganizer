import { Component, Renderer2 } from '@angular/core';
import { MatTabChangeEvent } from '@angular/material/tabs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  isDarkMode: boolean = false;

  constructor(private renderer: Renderer2) { 
    let isDarkMode = +localStorage.getItem('darkMode')!;

    if(isDarkMode === 0){
      this.setDarkMode();
    }else{
      this.setLightMode();
    }
  }

  setDarkMode(){
    this.isDarkMode = true;
    localStorage.setItem('darkMode', "0");

    this.renderer.addClass(document.body, 'theme-alternate');
  }

  setLightMode(){
    this.isDarkMode = false;
    localStorage.setItem('darkMode', "1");

    this.renderer.removeClass(document.body, 'theme-alternate');
  }
}
