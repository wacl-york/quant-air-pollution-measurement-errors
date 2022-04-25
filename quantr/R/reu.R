#' Calculates the Relative Expanded Uncertainty of low-cost sensor measurements when compared with a reference instrument.
#'
#' Foo TODO include detail of different methods
#'
#' @param ref Reference measurements
#' @param lcs Low-cost-sensor measurements
#' @param alpha Multiplier of standard error in relative uncertainty to obtain the expanded uncertainty. Defaults to 2 standard deviations.
#' @param u_ref Relative uncertainty of the reference instrument
#' @param lambda TODO
#' @param method Which of the 3 REU calculation methods to use. TODO
#' @return A vector of the same length as \code{ref} and \code{lcs} containing the corresponding REU estimates.
#' @examples
#' # Create dummy data frame
#' n_vals <- 100
#' df <- data.frame(timestamp=seq.POSIXt(from=as.POSIXct("2020-09-24 09:00:00"),
#'                                       to=as.POSIXct("2020-09-30 09:00:00"),
#'                                       length.out=n_vals),
#'                  ref=rnorm(n_vals, 30, 5),
#'                  lowcost=rnorm(n_vals, 32, 8))
#'
#' reu(df$ref, df$lowcost)
#'
#' @export
reu <- function(ref, lcs, alpha=2, u_ref = 0, lambda=1, method = c('GDE', 'NILU1', 'NILU2')) {
    stopifnot(length(ref) == length(lcs))
    method <- match.arg(method)

    #NOTE: Sigma_err_x (NILU notation) is the same as u_xi (GDE2010 notation)
    Sigma_err_x <- u_ref

    # Calculate useful statistics
    n <- length(ref)
    x_mean <- mean(ref, na.rm=T)
    y_mean <- mean(lcs, na.rm=T)
    S_x <- var(ref, na.rm=T)
    S_y <- var(lcs, na.rm=T)
    S_xy <- mean(ref*lcs, na.rm=T) - (x_mean * y_mean)

    #First step calculation of Slope and Intercept (bo & b1)
    #Slope (coeficient b1)
    btilde_1 <- (S_y - lambda*S_x + ((S_y - S_x)**2 + 4*lambda*(S_xy**2))**(1/2))/(2*S_xy)
    #Intercept (coeficient bo):
    btilde_0 <- y_mean - btilde_1*x_mean
    if (method == 'GDE') {
        #Equation error variance for y = b0 + b1*x + v_i
        rss <- (lcs - btilde_0 - btilde_1*ref)**2
        RSS <- sum(rss, na.rm=T)
        Sigma_v_sqr <- RSS/(n-2)
        #Error variance due to the deviation of the 1:1 line
        ec <- (btilde_0 + (btilde_1 - 1)*ref)**2
        REU <- (alpha/lcs)*((Sigma_v_sqr - Sigma_err_x**2 + ec)**(1/2))*100
    } else {
        #Equation error variance for Y = b0 + b1*X + u_i
        v_i <- lcs - btilde_0 - btilde_1*ref #Eq. Error
        RSS_c <- sum(v_i**2 - (btilde_1**2 + lambda)*Sigma_err_x**2, na.rm=T)
        Sigma_u_sqr <- RSS_c/(n-2)
        #Second step calculation of Slope and Intercept (Bo & B1)
        #Slope (coeficiente B1)
        B1 <- (S_y - lambda*S_x - Sigma_u_sqr + ((S_y - lambda*S_x - Sigma_u_sqr)**2 + 4*lambda*(S_xy**2))**(1/2))/(2*S_xy)
        #Intercept (coeficiente Bo):
        B0 <- y_mean - B1*x_mean
        #Error variance due to the deviation of the 1:1 line
        ec <- (B0 + (B1 - 1)*ref)**2
        if (method == 'NILU1') {
            #Equation error variance for y = B0 + B1*x + v_i
            rss <- (lcs - B0 - B1*ref)**2
            RSS <- sum(rss, na.rm=T)
            Sigma_v_sqr <- RSS / (n-2)
            REU <- (alpha/lcs) * ((Sigma_v_sqr - Sigma_err_x**2 + ec)**(1/2))*100   #Percentage
        } else if (method == 'NILU2') {
            #Measurement error variance corrected
            mec <- (lambda - (B1 - 1)**2)*Sigma_err_x**2
            REU <- (alpha/lcs) * ((Sigma_u_sqr + mec + ec)**(1/2))*100   #Percentage
        }
    }
    REU
}
