import { Component, OnInit, Input, Output, EventEmitter, OnChanges, SimpleChanges   } from '@angular/core';
import { throwError } from "rxjs";
import { TurnService} from "../turn.service";

@Component({
  selector: 'app-hand',
  templateUrl: './hand.component.html',
  styleUrls: ['./hand.component.css']
})
export class HandComponent implements OnInit, OnChanges{

  imgSrc: String = "/angular/app/assets/one-a-l.png";
  numberToString: string = 'one';
  rightLeftAbrv: string = 'r';
  imageBase: string = "/static/angular/app/assets/";

  @Input()
  orientation: string = '';

  @Input()
  flip: Boolean = false;

  @Input()
  fingers: number = 1;

  @Output()
  handClicked: EventEmitter<string> = new EventEmitter();

  constructor(private turnSrv: TurnService) {

  }

  ngOnChanges(changes: SimpleChanges): void
  {
    for( let property in changes)
    {
      if(property === 'fingers')
      {
        switch(changes[property].currentValue)
        {
          case 0:
            this.numberToString = "zero";
            break;
          case 1:
            this.numberToString = "one";
            break;
          case 2:
            this.numberToString = "two";
            break;
          case 3:
            this.numberToString = "three";
            break;
          case 4:
            this.numberToString = "four";
          break;
          default:
            throwError("Bad finger value must be between 0 and 4");
        }
        this.imgSrc = this.imageBase+this.numberToString+"-a-"+this.rightLeftAbrv+".png";
      }
    }
  }

  ngOnInit(): void {

      switch(this.orientation)
      {
        case "left":
          this.imgSrc = this.imageBase+"one-a-l.png";
          this.rightLeftAbrv = 'l';
        break;

        case "right":
          this.imgSrc = this.imageBase+"one-a-r.png";
          this.rightLeftAbrv = 'r';
        break;

        default:
          throwError("Hand orientation must be left or right.");
      }

  }

  handClick(){
    if( this.fingers == 0){
      console.log('you can not click on a knocked out hand')
      alert('you can on click on a knocked out hand')
      return
    }
    this.handClicked.emit(this.orientation);
  }

}
