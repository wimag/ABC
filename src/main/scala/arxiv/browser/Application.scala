package arxiv.browser

import akka.actor.ActorSystem
import akka.event.Logging
import akka.http.scaladsl.Http
import akka.http.scaladsl.server.directives.DebuggingDirectives
import akka.stream.ActorMaterializer


object Application extends App with Config with Routes {
  override implicit val system = ActorSystem()
  override implicit val executor = system.dispatcher
  override implicit val materializer = ActorMaterializer()

  protected val log = Logging(system, getClass)

  Http().bindAndHandle(
    handler = DebuggingDirectives.logRequestResult("log")(routes),
    interface = httpInterface, port = httpPort
  )
}

