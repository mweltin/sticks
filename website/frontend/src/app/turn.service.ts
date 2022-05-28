import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { ActionQueue } from './action-queue';
import {stringify} from "@angular/compiler/src/util";

@Injectable({
  providedIn: 'root'
})

export class TurnService {

   private currentPlayMessage = new BehaviorSubject('');
   public currentPlay = this.currentPlayMessage.asObservable();

  constructor(private http: HttpClient) { }

  private turnEndpoint = '/turn';

  takeATurn(turnData: ActionQueue){
    if( turnData.activePlayer == 'human'){
      let human_hand_value = turnData.human.activeHand == 'left' ? turnData.human.playerState[0]: turnData.human.playerState[1]
      let qlearning_hand_value = turnData.qlearning.activeHand == 'left' ? turnData.qlearning.playerState[0]: turnData.qlearning.playerState[1]
      this.updatePlayMessage("human: "+turnData.human.activeHand+ "("+human_hand_value+") to qlearning " + turnData.qlearning.activeHand + "("+qlearning_hand_value+")")
    }
    return this.http.post(this.turnEndpoint, {turnData});
  }

  public updatePlayMessage(message: string) {
    this.currentPlayMessage.next(message)
  }

}
