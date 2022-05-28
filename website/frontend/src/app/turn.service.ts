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
    return this.http.post(this.turnEndpoint, {turnData});
  }

  public updatePlayMessage(message: string) {
    this.currentPlayMessage.next(message)
  }

}
