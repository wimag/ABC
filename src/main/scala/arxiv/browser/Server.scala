package arxiv.browser

import akka.actor.ActorSystem
import akka.http.scaladsl.Http
import akka.http.scaladsl.model._
import akka.http.scaladsl.server.Directives._
import akka.stream.ActorMaterializer
import scala.io.StdIn


object WebServer {
  def main(args: Array[String]): Unit = {
    println("Starting server")

    implicit val system = ActorSystem()
    implicit val materializer = ActorMaterializer()
    implicit val executionContext = system.dispatcher

    val route =
      path("") {
        get {
          complete("ok")
        }
      }

    val serverBinding = Http().bindAndHandle(route, "localhost", 4242)
    println("Server started at 4242")

    StdIn.readLine()
    serverBinding.flatMap(_.unbind()).onComplete(_ => system.terminate())
  }

}
