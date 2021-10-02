import { Component, OnInit, Input } from '@angular/core';
import { throwError } from "rxjs";
@Component({
  selector: 'app-hand',
  templateUrl: './hand.component.html',
  styleUrls: ['./hand.component.css']
})
export class HandComponent implements OnInit {

  imgSrc: String = "/angular/app/assets/one-a-l.png";

  @Input()
  orientation: string = '';

  constructor() { 
  }

  ngOnInit(): void {

      switch(this.orientation)
      {
        case "left":
          this.imgSrc = "/static/angular/app/assets/one-a-l.png";
        break;

        case "right":
          this.imgSrc = "/static/angular/app/assets/one-a-r.png";
        break;

        default:
          throwError("Hand orientation must be left or right.");
      }

      
  }

  handClick(){
    alert("has been clicked");
  }

}
