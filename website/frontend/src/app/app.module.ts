import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HandComponent } from './hand/hand.component';
import { PlayerComponent } from './player/player.component';
import { GameComponent } from './game/game.component';
import { TurnService } from './turn.service';

@NgModule({
  declarations: [
    AppComponent,
    HandComponent,
    PlayerComponent,
    GameComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [
    TurnService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
