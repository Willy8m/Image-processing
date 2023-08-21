# Analysis of the paper: A new k out of n secret image sharing scheme in visual cryptography

This is the final project of the course "Image Processing and Artificial Vision" from the Physics degree imparted at UB. In the code directory, you will find both the code to demonstrate the flaws of the method, and the code to create an nth-order Shamir polynomial. In the "Papers" directory you will find both Shakar's paper and our analysis report. 

## About the project

> Visual Cryptography (VC) is a security technique consisting of encoding an image by dividing it up into a certain number of shares and distributing them among various participants. It is essential to amass all the shares in order to decrypt the original image, with two participants we would have:

[![Visual criptography](https://www.101computing.net/wp/wp-content/uploads/visual-cryptography-of-space-invader.png "Visual criptography")](https://www.101computing.net/wp/wp-content/uploads/visual-cryptography-of-space-invader.png "Visual criptography")

> In a "k out of n" (k,n) scheme, only k<n shares need to be known in order to recover the final image. This represents a big leap forward in VC, providing versatility and security in comparison to current methods.

[![k out of n VC](https://media.springernature.com/lw685/springer-static/image/art%3A10.1007%2Fs11042-021-11229-9/MediaObjects/11042_2021_11229_Fig1_HTML.png "k out of n VC")](https://media.springernature.com/lw685/springer-static/image/art%3A10.1007%2Fs11042-021-11229-9/MediaObjects/11042_2021_11229_Fig1_HTML.png "k out of n VC")

> In this paper, we explore Shakar and Swaran's (k,n) technique, the structural and security flaws of which are discussed. In addition, a working solution using Shamir's polynomial is proposed, which would actually solve the (k,n) problem for VC.
